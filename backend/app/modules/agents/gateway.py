import httpx

from app.core.config import settings


class ModelGatewayError(Exception):
    pass


class ModelGatewayUnavailable(ModelGatewayError):
    pass


class ModelGateway:
    def complete(
        self,
        *,
        model: str,
        system_prompt: str,
        prompt: str,
        memory: list[str],
    ) -> str:
        if not settings.model_gateway_url or not settings.model_gateway_api_key:
            raise ModelGatewayUnavailable(
                "Model gateway is not configured. Set MODEL_GATEWAY_URL and MODEL_GATEWAY_API_KEY."
            )

        base_urls = [settings.model_gateway_url]
        if settings.model_gateway_fallback_urls:
            base_urls.extend(settings.model_gateway_fallback_urls.split(","))

        context = "\n\n".join(memory)
        user_content = prompt
        if context:
            user_content = f"Relevant agent memory:\n{context}\n\nUser request:\n{prompt}"

        last_error: ModelGatewayError | None = None
        for index, base_url in enumerate(base_urls):
            try:
                response = httpx.post(
                    f"{base_url}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.model_gateway_api_key}"},
                    json={
                        "model": model,
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content},
                        ],
                    },
                    timeout=settings.model_gateway_timeout_seconds,
                )
                response.raise_for_status()
            except httpx.TimeoutException as exc:
                last_error = ModelGatewayUnavailable("Model gateway request timed out.")
                if index + 1 < len(base_urls):
                    continue
                raise last_error from exc
            except httpx.HTTPStatusError as exc:
                status_code = exc.response.status_code
                last_error = ModelGatewayError(
                    f"Model gateway returned HTTP {status_code}."
                )
                if status_code in (408, 429) or status_code >= 500:
                    if index + 1 < len(base_urls):
                        continue
                raise last_error from exc
            except httpx.RequestError as exc:
                last_error = ModelGatewayUnavailable(
                    "Could not connect to the configured model gateway."
                )
                if index + 1 < len(base_urls):
                    continue
                raise last_error from exc

            try:
                content = response.json()["choices"][0]["message"]["content"]
            except (ValueError, KeyError, IndexError, TypeError) as exc:
                raise ModelGatewayError(
                    "Model gateway returned an invalid completion response."
                ) from exc

            if not isinstance(content, str) or not content.strip():
                raise ModelGatewayError("Model gateway returned an empty completion.")
            return content.strip()

        raise last_error or ModelGatewayUnavailable("No model gateway route is available.")

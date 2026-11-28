$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
& (Join-Path $PSScriptRoot 'bootstrap-local.ps1')

Push-Location $repositoryRoot
try {
    docker compose --env-file .env up --build -d
    if ($LASTEXITCODE -ne 0) {
        throw 'Docker Compose could not start the local services.'
    }

    $ready = $false
    for ($attempt = 0; $attempt -lt 60; $attempt++) {
        try {
            $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8765/health' -TimeoutSec 3
            if ($health.status -eq 'healthy') {
                $ready = $true
                break
            }
        }
        catch {
            Start-Sleep -Seconds 2
        }
    }

    if (-not $ready) {
        docker compose --env-file .env logs --tail 100 api
        throw 'The API did not become healthy. Review the API logs above.'
    }
}
finally {
    Pop-Location
}

Write-Output 'ApexiveAI is ready at http://127.0.0.1:8765'
Write-Output 'API documentation: http://127.0.0.1:8765/docs'
Write-Output 'This local prototype has no authentication; do not expose it to a network.'

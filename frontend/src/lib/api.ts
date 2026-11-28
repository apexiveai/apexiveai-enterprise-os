const apiBaseUrl = (import.meta.env.VITE_API_URL || '').trim().replace(/\/+$/, '')

export function apiUrl(path: string): string {
  if (!apiBaseUrl) return path

  const normalizedPath = path.startsWith('/') ? path : `/${path}`
  return `${apiBaseUrl}${normalizedPath}`
}

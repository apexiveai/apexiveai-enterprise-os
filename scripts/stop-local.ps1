$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
Push-Location $repositoryRoot
try {
    docker compose --env-file .env stop
    if ($LASTEXITCODE -ne 0) {
        throw 'Docker Compose could not stop the local services.'
    }
}
finally {
    Pop-Location
}

Write-Output 'Local services stopped. Database, Redis, and object-storage volumes were preserved.'

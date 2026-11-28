$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path -Parent $PSScriptRoot
$environmentFile = Join-Path $repositoryRoot '.env'
$exampleFile = Join-Path $repositoryRoot '.env.example'
$passwordPlaceholder = 'generate-locally-with-scripts-bootstrap-local.ps1'
$databasePlaceholder = 'postgresql+psycopg://max:replace-with-bootstrap-password@localhost:5432/max_enterprise'

if (-not (Test-Path -LiteralPath $environmentFile)) {
    Copy-Item -LiteralPath $exampleFile -Destination $environmentFile
}

$lines = [System.Collections.Generic.List[string]]::new()
[System.IO.File]::ReadAllLines($environmentFile) | ForEach-Object { $lines.Add($_) }

$passwordIndex = -1
$databaseIndex = -1
$tenantIndex = -1
for ($index = 0; $index -lt $lines.Count; $index++) {
    if ($lines[$index] -match '^\s*POSTGRES_PASSWORD\s*=') { $passwordIndex = $index }
    if ($lines[$index] -match '^\s*DATABASE_URL\s*=') { $databaseIndex = $index }
    if ($lines[$index] -match '^\s*VITE_TENANT_ID\s*=') { $tenantIndex = $index }
}

$passwordIsPlaceholder = $passwordIndex -lt 0 -or
    $lines[$passwordIndex] -match '^\s*POSTGRES_PASSWORD\s*=\s*generate-locally-with-scripts-bootstrap-local\.ps1\s*$'

if ($passwordIsPlaceholder) {
    $randomBytes = New-Object byte[] 32
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $generator.GetBytes($randomBytes)
    }
    finally {
        $generator.Dispose()
    }
    $password = [System.BitConverter]::ToString($randomBytes).Replace('-', '').ToLowerInvariant()
    $passwordLine = "POSTGRES_PASSWORD=$password"

    if ($passwordIndex -lt 0) {
        $lines.Add($passwordLine)
    }
    else {
        $lines[$passwordIndex] = $passwordLine
    }

    if ($databaseIndex -ge 0 -and $lines[$databaseIndex] -eq "DATABASE_URL=$databasePlaceholder") {
        $lines[$databaseIndex] = "DATABASE_URL=postgresql+psycopg://max:$password@localhost:5432/max_enterprise"
    }
}

if ($tenantIndex -lt 0) {
    $lines.Add('VITE_TENANT_ID=local-workspace')
}

$encoding = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllLines($environmentFile, $lines, $encoding)
Write-Output 'Local environment is ready. Existing configured values were preserved.'

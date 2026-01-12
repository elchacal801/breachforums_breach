<#
.SYNOPSIS
Securely imports the BreachForums MyBB dump into a disposable Docker container.
.DESCRIPTION
This script acts as the primary interface for data loading. It:
1. Checks for the data file.
2. Spins up a MySQL 8 container (isolated).
3. Imports the SQL dump.
4. Verifies row counts against the expected 323,986.
#>

$ErrorActionPreference = "Stop"
$DataDir = Join-Path $PSScriptRoot "../data"
$SqlFile = Join-Path $DataDir "databoose.sql"
$ContainerName = "bf-mysql-analysis"
$DbName = "bf"
$DbUser = "root"
$DbPass = "research_only" # Ephemeral password for local container

Write-Host "[*] BreachForums Analysis Environment Setup" -ForegroundColor Cyan

# 1. Check Prereqs
if (-not (Test-Path $SqlFile)) {
    Write-Error "Data file not found at: $SqlFile`nPlease ensure you have placed 'databoose.sql' in the 'data' directory."
}

# 2. Docker Management
if (docker ps -a --format '{{.Names}}' | Select-String -Quiet $ContainerName) {
    Write-Host "[!] Container $ContainerName already exists. Removing..." -ForegroundColor Yellow
    docker rm -f $ContainerName | Out-Null
}

Write-Host "[+] Starting MySQL 8 container..." -ForegroundColor Green
# Simple networking, no volume persistence for safety (ephemeral)
docker run --name $ContainerName -e MYSQL_ROOT_PASSWORD=$DbPass -d mysql:8

Write-Host "[+] Waiting for MySQL to initialize (15s)..."
Start-Sleep -Seconds 15

# 3. Create DB
Write-Host "[+] Creating database '$DbName'..."
docker exec -i $ContainerName mysql -u$DbUser -p$DbPass -e "CREATE DATABASE IF NOT EXISTS $DbName;"

# 4. Import
Write-Host "[+] Importing SQL dump (this may take a minute)..." -ForegroundColor Green
Get-Content $SqlFile | docker exec -i $ContainerName mysql -u$DbUser -p$DbPass $DbName

# 5. Verify
Write-Host "[+] Verifying integrity..." -ForegroundColor Cyan
$CountQuery = "SELECT COUNT(*) FROM hcclmafd2jnkwmfufmybb_users;"
$Result = docker exec -i $ContainerName mysql -u$DbUser -p$DbPass $DbName -N -e $CountQuery

$Expected = 323986
if ([int]$Result -eq $Expected) {
    Write-Host "[SUCCESS] Row count matches expected: $Result" -ForegroundColor Green
}
else {
    Write-Host "[WARNING] Row count MISMATCH. Expected: $Expected, Got: $Result" -ForegroundColor Red
}

Write-Host "`n[INFO] Environment ready. You can now run analysis queries."
Write-Host "Example: docker exec -i $ContainerName mysql -u$DbUser -p$DbPass $DbName < queries/metrics.sql"

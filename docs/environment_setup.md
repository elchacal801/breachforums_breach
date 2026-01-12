# Environment Setup

## Prerequisites

- Windows 11 / 10
- Docker Desktop (WSL2 Backend enabled)
- PowerShell 7+

## Quick Start

1. Ensure `databoose.sql` is in `data/` (create this folder if missing; it is gitignored).
2. Run the import script:

   ```powershell
   ./scripts/import_to_docker.ps1
   ```

   This will:
   - Pull `mysql:8` image.
   - Start container `bf-mysql-analysis`.
   - Create database `bf`.
   - Import the sql file.
   - Run verification checks.

## Manual Commands (Reference)

If the script fails, you can run manually:

```bash
docker run --name bf-mysql -e MYSQL_ROOT_PASSWORD=research -p 3306:3306 -d mysql:8
docker cp data/databoose.sql bf-mysql:/tmp/dump.sql
docker exec -i bf-mysql mysql -uroot -presearch -e "CREATE DATABASE bf; USE bf; SOURCE /tmp/dump.sql;"
```

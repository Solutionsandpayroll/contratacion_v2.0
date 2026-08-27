$ErrorActionPreference = "Stop"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $scriptDir

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  CONTRATACION V2.0 - Setup & Run" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# 1. Cargar variables de entorno desde .env
Write-Host "`n[1/6] Cargando variables de entorno..." -ForegroundColor Yellow
$envFile = Join-Path $scriptDir ".env"
if (Test-Path -LiteralPath $envFile) {
    Get-Content -LiteralPath $envFile | ForEach-Object {
        if ($_ -match "^\s*([^#][^=]+?)\s*=\s*(.+)\s*$") {
            $name = $matches[1].Trim()
            $value = $matches[2].Trim()
            [Environment]::SetEnvironmentVariable($name, $value, "Process")
            Write-Host "  * $name = $value" -ForegroundColor DarkGray
        }
    }
    Write-Host "  Variables cargadas correctamente." -ForegroundColor Green
} else {
    Write-Host "  ADVERTENCIA: No se encontro el archivo .env" -ForegroundColor Red
}

# 2. Crear entorno virtual si no existe
Write-Host "`n[2/6] Verificando entorno virtual..." -ForegroundColor Yellow
$venvPath = Join-Path $scriptDir ".venv"
if (-not (Test-Path -LiteralPath $venvPath)) {
    Write-Host "  Creando entorno virtual..." -ForegroundColor Gray
    python -m venv $venvPath
    Write-Host "  Entorno virtual creado." -ForegroundColor Green
} else {
    Write-Host "  Entorno virtual ya existe." -ForegroundColor Green
}

# 3. Activar entorno virtual
Write-Host "`n[3/6] Activando entorno virtual..." -ForegroundColor Yellow
$activatePath = Join-Path $venvPath "Scripts\Activate.ps1"
& $activatePath
Write-Host "  Entorno virtual activado." -ForegroundColor Green

# 4. Instalar dependencias
Write-Host "`n[4/6] Instalando dependencias..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet
Write-Host "  Dependencias instaladas." -ForegroundColor Green

# 5. Preparar la base de datos
Write-Host "`n[5/6] Preparando base de datos..." -ForegroundColor Yellow
Set-Location -LiteralPath (Join-Path $scriptDir "app")
python manage.py makemigrations --noinput 2>&1 | Out-Null
python manage.py migrate --noinput
Write-Host "  Migraciones aplicadas." -ForegroundColor Green

Write-Host "  Recopilando archivos estaticos..." -ForegroundColor Gray
python manage.py collectstatic --noinput 2>&1 | Out-Null
Write-Host "  Estaticos recopilados." -ForegroundColor Green

# 6. Iniciar servidor
Write-Host "`n[6/6] Iniciando servidor Django..." -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Login:            http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "  Panel empleados:  http://127.0.0.1:8000/empleados/panel/" -ForegroundColor White
Write-Host "  Admin Django:     http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "`nPresiona Ctrl+C para detener el servidor.`n" -ForegroundColor DarkGray

python manage.py runserver 0.0.0.0:8000

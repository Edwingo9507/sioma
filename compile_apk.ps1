# Script de PowerShell para compilar SINOMA APK usando WSL
# Ejecutar: .\compile_apk.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPILACION DE SINOMA APK VIA WSL" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que WSL está instalado
Write-Host "[1/3] Verificando WSL..." -ForegroundColor Yellow
try {
    $wslVersion = wsl --version 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "WSL no esta instalado o no esta configurado correctamente"
    }
    Write-Host "WSL detectado" -ForegroundColor Green
} catch {
    Write-Host "Error: WSL no esta instalado" -ForegroundColor Red
    Write-Host ""
    Write-Host "Para instalar WSL:" -ForegroundColor Yellow
    Write-Host "  1. Abre PowerShell como Administrador"
    Write-Host "  2. Ejecuta: wsl --install"
    Write-Host "  3. Reinicia tu PC"
    Write-Host "  4. Configura Ubuntu (usuario y contraseña)"
    Write-Host "  5. Vuelve a ejecutar este script"
    exit 1
}
Write-Host ""

# Verificar archivos necesarios
Write-Host "[2/3] Verificando archivos del proyecto..." -ForegroundColor Yellow
$requiredFiles = @("main.py", "builder.spec", "logo.png", "data\haarcascade_frontalface_default.xml")
$allFilesExist = $true

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  OK: $file" -ForegroundColor Green
    } else {
        Write-Host "  FALTA: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

if (-not $allFilesExist) {
    Write-Host ""
    Write-Host "Faltan archivos necesarios. Verifica tu proyecto." -ForegroundColor Red
    exit 1
}
Write-Host ""

# Convertir path de Windows a WSL
$currentPath = (Get-Location).Path
$wslPath = $currentPath -replace '\\', '/' -replace ':', '' -replace '^([A-Z])', '/mnt/$1'
$wslPath = $wslPath.ToLower()

Write-Host "[3/3] Iniciando compilación en WSL..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Ruta WSL: $wslPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANTE:" -ForegroundColor Yellow
Write-Host "  - La primera compilación tarda 30-60 minutos" -ForegroundColor White
Write-Host "  - Se descargarán ~1.5 GB" -ForegroundColor White
Write-Host "  - Se necesitan ~10 GB libres" -ForegroundColor White
Write-Host "  - Se te pedirá la contraseña de WSL varias veces (para sudo)" -ForegroundColor White
Write-Host ""
Write-Host "Presiona ENTER para continuar o Ctrl+C para cancelar..."
$null = Read-Host

Write-Host ""
Write-Host "Ejecutando script de compilacion en WSL..." -ForegroundColor Cyan
Write-Host ""

# Ejecutar en WSL con distribución Ubuntu específica usando bash
wsl -d Ubuntu bash compile_apk_wsl.sh

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  COMPILACION COMPLETADA" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "El APK deberia estar en: bin\" -ForegroundColor Cyan
    
    # Listar APKs generados
    if (Test-Path "bin\*.apk") {
        Write-Host ""
        Write-Host "APKs generados:" -ForegroundColor Cyan
        Get-ChildItem bin\*.apk | ForEach-Object {
            $sizeMB = [math]::Round($_.Length/1MB, 2)
            Write-Host "  APK: $($_.Name) ($sizeMB MB)" -ForegroundColor White
        }
    }
    
    Write-Host ""
    Write-Host "Para instalar en Android:" -ForegroundColor Yellow
    Write-Host "  1. Copia el APK a tu telefono" -ForegroundColor White
    Write-Host "  2. Habilita Fuentes desconocidas" -ForegroundColor White
    Write-Host "  3. Abre el APK e instala" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERROR EN COMPILACION" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Revisa los mensajes de error arriba" -ForegroundColor Yellow
    Write-Host ""
    exit 1
}

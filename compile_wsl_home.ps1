# Script PowerShell para compilar desde WSL home (sin espacios en ruta)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  COMPILAR APK DESDE WSL HOME" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Este script copia el proyecto a ~/sioma_build en WSL" -ForegroundColor Yellow
Write-Host "para evitar el error de espacios en la ruta." -ForegroundColor Yellow
Write-Host ""
Write-Host "Presiona ENTER para continuar..."
$null = Read-Host

# Ejecutar script en WSL
wsl -d Ubuntu bash compile_from_wsl_home.sh

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  COMPILACION EXITOSA" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    
    # Mostrar APKs si existen
    if (Test-Path "bin\*.apk") {
        Write-Host "APKs generados:" -ForegroundColor Cyan
        Get-ChildItem bin\*.apk | ForEach-Object {
            $sizeMB = [math]::Round($_.Length/1MB, 2)
            Write-Host "  $($_.Name) - $sizeMB MB" -ForegroundColor White
        }
    }
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ERROR EN COMPILACION" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
}

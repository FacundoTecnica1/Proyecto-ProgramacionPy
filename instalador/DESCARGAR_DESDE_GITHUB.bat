@echo off
title Instalador GitHub - Juego Dinosaurio
color 0A

echo.
echo     🦖 INSTALADOR AUTOMÁTICO DESDE GITHUB 🦖
echo.
echo ========================================================
echo    DESCARGA E INSTALA AUTOMÁTICAMENTE EL JUEGO
echo ========================================================
echo.

REM Verificar Python
echo [1/2] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo.
    echo ❌ ERROR: Python no esta instalado
    echo.
    echo 📥 SOLUCION:
    echo    1. Ve a: https://www.python.org/downloads/
    echo    2. Descarga Python 3.8 o superior
    echo    3. Durante la instalacion, marca "Add Python to PATH"
    echo    4. Reinicia este instalador
    echo.
    pause
    exit /b 1
)

echo ✅ Python detectado correctamente
echo.

REM Verificar conexión a internet
echo [2/2] Verificando conexión a internet...
ping google.com -n 1 >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ❌ ERROR: Sin conexión a internet
    echo    Verifica tu conexión y vuelve a intentar
    pause
    exit /b 1
)

echo ✅ Conexión a internet verificada
echo.

color 0B
echo 🌐 INICIANDO DESCARGA DESDE GITHUB...
echo.
echo    • Se descargará el proyecto completo automáticamente
echo    • Se extraerán todos los archivos
echo    • Se ejecutará el instalador premium
echo    • El proceso puede tardar 5-15 minutos
echo.

timeout /t 3 /nobreak >nul

REM Ejecutar instalador de GitHub
python instalador_github.py

REM Verificar resultado
if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ✅ Proceso completado correctamente
) else (
    color 0C
    echo.
    echo ❌ Error en el proceso de descarga
)

echo.
pause
@echo off
title Instalador Premium - Juego Dinosaurio
color 0A

echo.
echo     ████████╗  ████████╗  ████████╗  ████████╗
echo     ██╔════██╗ ██╔════██╗ ██╔════██╗ ██╔════██╗
echo     ██║    ██║ ██║    ██║ ██║    ██║ ██║    ██║
echo     ██║    ██║ ██║    ██║ ██║    ██║ ██║    ██║
echo     ████████╔╝ ████████╔╝ ████████╔╝ ████████╔╝
echo     ╚═══════╝  ╚═══════╝  ╚═══════╝  ╚═══════╝
echo.
echo     🦖 INSTALADOR PREMIUM JUEGO DINOSAURIO 🦖
echo.
echo ========================================================
echo    INSTALACION AUTOMATICA CON INTERFAZ GRAFICA
echo ========================================================
echo.

REM Verificar Python
echo [1/3] Verificando Python...
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

REM Verificar archivos necesarios
echo [2/3] Verificando archivos del instalador...
if not exist "instalador_premium.py" (
    color 0C
    echo ❌ ERROR: No se encontro instalador_premium.py
    echo Asegurate de ejecutar este archivo desde la carpeta 'instalador'
    pause
    exit /b 1
)

echo ✅ Archivos verificados
echo.

REM Lanzar instalador grafico
echo [3/3] Iniciando instalador grafico...
echo.
echo 🚀 Abriendo instalador con interfaz grafica...
echo    - El instalador aparecera en una nueva ventana
echo    - Sigue las instrucciones en pantalla
echo    - La instalacion es completamente automatica
echo.

color 0B
echo ⚡ LANZANDO INSTALADOR PREMIUM...
timeout /t 2 /nobreak >nul

REM Ejecutar instalador premium
python instalador_premium.py

REM Verificar resultado
if %errorlevel% equ 0 (
    color 0A
    echo.
    echo ✅ Instalador ejecutado correctamente
) else (
    color 0C
    echo.
    echo ❌ Error al ejecutar el instalador
    echo.
    echo 🔧 POSIBLES SOLUCIONES:
    echo    1. Ejecuta como administrador
    echo    2. Verifica que Python este instalado correctamente
    echo    3. Instala dependencias: pip install tkinter
)

echo.
pause
@echo off
title Bot Coca-Cola - Iniciando...

:: Verificar que Python esté instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no está instalado en esta PC.
    echo Descargalo desde https://www.python.org/downloads/
    echo Asegúrate de marcar "Add Python to PATH" al instalar.
    pause
    exit /b
)

:: Si el entorno virtual no existe, instalarlo por primera vez
if not exist "venv\" (
    echo Primera vez detectada. Instalando todo...
    echo.
    python -m venv venv
    call .\venv\Scripts\activate.bat
    pip install python-telegram-bot openpyxl
    echo.
    echo Instalacion completada!
    echo.
) else (
    echo Entorno ya instalado. Iniciando bot...
    echo.
)

:: Correr el bot en segundo plano via VBS
wscript.exe iniciar_bot.vbs

echo El bot esta corriendo en segundo plano.
echo Para detenerlo usa detener_bot.bat
echo.
pause

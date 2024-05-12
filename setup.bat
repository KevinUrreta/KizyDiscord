@echo off

cls

echo Descargando e instalando Chocolatey...
@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin"

echo.
echo Verificando la instalación de Chocolatey...
choco -v

pause

rem Actualizar lista de paquetes
echo Actualizando lista de paquetes...
choco update

rem Buscar el paquete ffmpeg
echo Buscando el paquete ffmpeg...
choco search ffmpeg

rem Instalar ffmpeg
echo Instalando ffmpeg...
choco install ffmpeg -y

rem Verificar la ubicación de ffmpeg
echo Verificando la ubicación de ffmpeg...
where ffmpeg

rem No hay un equivalente directo en Windows para modificar .bashrc
rem Si necesitas hacer cambios en las variables de entorno, puedes hacerlo manualmente a través del Panel de Control o PowerShell.

rem Instalar las bibliotecas Python necesarias
echo Instalando bibliotecas Python necesarias...
pip install discord.py ffmpeg yt-dlp PyNaCl googletrans

rem Ejecutar el script de Python
echo Ya puedes ejecutar el script de Python

pause

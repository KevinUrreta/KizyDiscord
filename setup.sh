#!/bin/bash

# Actualizar lista de paquetes
sudo apt-get update

# Buscar el paquete ffmpeg
apt search ffmpeg

# Instalar ffmpeg
sudo apt-get install ffmpeg -y

# Verificar la ubicación de ffmpeg
which ffmpeg

# Abrir el archivo .bashrc en el editor nano (puedes cambiarlo por el editor que prefieras)
sudo nano ~/.bashrc

# Recargar el archivo .bashrc para aplicar los cambios
source ~/.bashrc

# Instalar las bibliotecas Python necesarias
pip install discord.py ffmpeg yt_dlp PyNaCl googletrans

# Ejecutar el script de Python
echo Ya puedes ejecutar el script de Python

# python3 -m pip install --upgrade yt-dlp -- Si no funciona al instalar
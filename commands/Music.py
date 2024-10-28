import discord; from discord.ext import commands
import spotipy; from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from datetime import datetime
import requests
import asyncio
import random
import json

async def setup(client :commands.Bot):
    await client.add_cog(Music(client))

def readDB():
    """ Abre un archivo en modo lectura. """
    try:
        with open("files/configuracion.json", "r", encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return {}

def writeDB(save):
    """ Abre un archivo en modo escritura """
    with open("files/configuracion.json", "w", encoding="utf-8") as f: json.dump(save, f, indent=4)

yt_dlp.utils.bug_reports_message = lambda: "" # Suprime los mensajes de error en consola.

# Opciones para el formato de youtube_dl o yt_dlp
ytdl_format_options = {
    "format": "bestaudio/best",  # Formato de audio preferido
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s",  # Plantilla de nombre de archivo de salida
    "restrictfilenames": True,  # Restringe los nombres de archivo para evitar caracteres especiales
    "noplaylist": False,  # Evita la descarga de listas de reproducción completas
    "nocheckcertificate": True,  # No comprueba los certificados SSL
    "ignoreerrors": False,  # Ignora los errores durante la descarga
    "logtostderr": False,  # No muestra registros en la salida estándar de error
    "quiet": True,  # Ejecución silenciosa, sin mensajes de estado en la salida estándar
    "no_warnings": True,  # Desactiva las advertencias de ytdl
    "default_search": "auto",  # Método de búsqueda predeterminado (auto, youtube, etc.)
    "source_address": "0.0.0.0",  # Dirección de origen para la conexión
    "extractaudio": True,  # Extrae solo el audio del video
    "audioformat": "mp3",  # Formato de audio de salida
    "preferredquality": "192",  # Calidad de audio preferida (en kbps)
    "cookiefile": "cookies.txt",  # Archivo de cookies para la autenticación
}

# Opciones de formato de sonido para ffmpeg
ffmpeg_options = {
    "options": "-vn",  # Solo se quedará con el audio, omitiendo el video
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",  # Reconexión automática en caso de desconexión
    # "format": "s16le",  # Formato de audio PCM de 16 bits, útil para algunas aplicaciones de transmisión de audio
    # "ar": "44100",  # Frecuencia de muestreo de audio (ejemplo: 44100 Hz)
    # "ac": "2",  # Número de canales de audio (ejemplo: 2 para estéreo)
    # "af": "bass=g=10",  # Filtro de audio para ajustar los graves (ejemplo: aumentar los graves)
    # "vn": True,  # Omitir el video por completo
    # "sn": True,  # Omitir la etiqueta de secuencia de número
    # "y": True,  # Sobrescribe archivos de salida sin preguntar
} 

ytdl = yt_dlp.YoutubeDL(ytdl_format_options) # yt_dlp o youtube_dl con las opciones agregadas.

# ===== Clase ========================================================================================== #

class YTDLSource(discord.PCMVolumeTransformer):
    """
    Define una clase para posteriormente buscar una canción en Youtube.
    """
    def __init__(self, source, *, data :dict, volume :float = 0.1) -> None:
        super().__init__(source, volume)

        self.data :dict = data
        self.title = data.get("title")
        self.url = data.get("url")
        self.original_url = data.get("original_url")
        self.thumbnail = data.get("thumbnail")
        self.duration = "{:.2f}".format(data.get("duration") / 60)
        self.duration_string = data.get("duration_string")
        self.views = data.get("view_count")

# ===== Método ================================ #

    @classmethod
    async def from_url(self, url:str, loop=None, stream :bool = False):
        """
        A partir del texto proporcionado, realiza una búsqueda y devuelve el audio.
        """
        # spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())
        try:
            loop = loop or asyncio.get_event_loop()
            # results = spotify.search(q=url, limit=1, type='track')
            # if results['tracks']['items']:
            #     track = results['tracks']['items'][0]
            #     track_url = track['preview_url']

            #     if track_url:
            #         # Descarga el audio y lo reproduce en el canal de voz
            #         return cls(discord.FFmpegPCMAudio(track_url, **ffmpeg_options))

            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
            with open("files/extract_info.json", "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            if "entries" in data:
                data = data["entries"][0] # Toma el 1º elemento de la lista de reproducción.

            filename = data['url'] if stream else ytdl.prepare_filename(data)
            return self(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

        except Exception as e:
            print(e)

# ===== Clase ========================================================================================== #

class Music(commands.Cog):
    """
    Comandos básicos de música en Discord.
    """
    def __init__(self, client) -> None:
        self.client :discord.Client = client
        self.playList :asyncio.Queue = asyncio.Queue()

# ===== Comando =============================== #

    @commands.command(name="join", help="Kizy se une al canal actual.")
    async def join(self, ctx :commands.Context, *, channel: discord.VoiceChannel):
        """
        Comprueba si el autor del mensaje está en canal de voz, y se mueve si así es.
        """
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

# ===== Comando =============================== #

    @commands.command(name="play", aliases=["p"], help="Reproduce una canción.")
    async def play(self, ctx:commands.Context, *, link :str = ""):
        """
        Busca la canción y lo añade a la lista, si esta ya sonando se añade en la cola,
        si el autor está en el canal y no está sonando se llama a la función.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        try:
            if link == "":
                kizy.add_field(name="Debes de insertar canción o enlace", value="No puedo reproducir música si no me dices que canción es.")
                return await ctx.send(embed=kizy)

            if link.startswith("https://open.spotify.com"):
                kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
                kizy.set_thumbnail(url="https://developer.spotify.com/images/guidelines/design/icon3@2x.png")
                kizy.add_field(name="¿Te gusta Spotify?", value=str(
                    "A mi también pero lamentablemente de momento aún no puedo reproducir música de esta plataforma.\n"
                    "Estamos trabajando para implementar esta función."
                    ))
                return await ctx.send(embed=kizy)

            song = await YTDLSource.from_url(url=link, loop=self.client.loop, stream=True)
            await self.playList.put((ctx, song))

            if ctx.voice_client.is_playing():
                kizy.add_field(name="Se ha añadido a la cola:", value=song.title, inline=False)
                kizy.add_field(name="En cola:", value=self.playList.qsize())
                kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
                kizy.set_thumbnail(url=song.thumbnail)
                return await ctx.send(embed=kizy)

            if not ctx.voice_client or not ctx.voice_client.is_playing():
                await self.nextSong(ctx)

        except Exception as e:
            print(e)

    async def nextSong(self, ctx :commands.Context):
        """
        Si la lista está vacía, no continua. Detiene la reproducción recoge los datos de la lista
        y reproduce la canción que se ha recogido de la lista, cuando suene se envía la canción
        sonando actualmente.
        """
        try:
            kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
            if self.playList.empty():
                kizy.add_field(name="La lista esta vacía", value="Se ha acabado tu playlist, me gustaba bastante tus gustos musicales.\n¿Pones más?")
                return await ctx.send(embed=kizy)

            if ctx.voice_client is None:
                kizy.add_field(name="¿Te has ido?", value="No me gusta estar sola :(")
                return await ctx.send(embed=kizy)

            ctx.voice_client.stop()
            ctx, song = await self.playList.get()
            ctx.voice_client.play(song, after=lambda: asyncio.run_coroutine_threadsafe(self.nextSong(ctx), self.client.loop))
            data :dict = readDB()
            volume = data[str(ctx.guild.id)]["volume"]
            ctx.voice_client.source.volume = volume

            kizy = discord.Embed(title="**Ahora suena**",color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name="**Título**:",value=f"{song.title}",inline=False)
            kizy.add_field(name="**Duración**:",value=f"{song.duration_string}min",inline=True)
            kizy.add_field(name="**Visitas**:",value=f"{song.views} visitas",inline=True)
            kizy.add_field(name="**En cola**:",value=self.playList.qsize(), inline=True)
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            kizy.set_thumbnail(url=song.thumbnail)

            vista = discord.ui.View()
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.red, label="Detener", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="Pausar", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="Saltar", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, label="Lista", disabled=True))
            await ctx.send(embed=kizy, view=vista)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="pause", help="Pausa la reproducción.")
    async def pause(self, ctx :commands.Context):
        """
        Si el autor está en el canal de voz, y está sonando, entonces pausa.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.pause()
                kizy.add_field(name="Se ha pausado la reproducción", value="¡Me estaba gustando la canción!")
                await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="resume", aliases=["continue"], help="Renauda la reproducción.")
    async def resume(self, ctx :commands.Context):
        """
        Pausa la reproduzcción actual de la lista.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if ctx.voice_client and ctx.voice_client.is_paused():
                ctx.voice_client.resume()
                kizy.add_field(name="Se ha renaudado la reproducción", value="¡Que bien! Me gusta mucho tu música.")
                await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="stop", help="Detiene la reproducción y limpia la cola.")
    async def stop(self, ctx :commands.Context):
        """
        Detiene la reproducción actual de la lista.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                self.playList :asyncio.Queue  = asyncio.Queue()

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="skip", help="Salta la reproducción actual.")
    async def skip(self, ctx :commands.Context):
        """
        Si está el autor está en el canal de voz, y si está sonando, entonces detiene la lista, y continua con el proximo en la cola.
        """
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await self.playList.join()  # Vacía la cola de reproducción

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="nowplaying", help="Muestra la reproducción actual.")
    async def nowplaying(self, ctx :commands.Context):
        """
        Devuelve la canción que este sonando actualmente en la lista de reproducción.
        """
        if ctx.voice_client is not None:
            ctx, song = await self.playList.get()

            kizy = discord.Embed(title="**Ahora suena**",color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name="**Título**:",value=f"{song.title}",inline=False)
            kizy.add_field(name="**Duración**:",value=f"{song.duration_string}min",inline=True)
            kizy.add_field(name="**Visitas**:",value=f"{song.views} visitas",inline=True)
            kizy.add_field(name="**En cola**:",value=self.playList.qsize(), inline=True)
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            kizy.set_thumbnail(url=song.thumbnail)

            vista = discord.ui.View()
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.red, label="Detener", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.green, label="Pausar", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, label="Saltar", disabled=True))
            vista.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, label="Lista", disabled=True))
        try:
            return await ctx.send(embed=kizy, view=vista)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="remove", help="Elimina una canción de la cola.")
    async def remove(self, ctx: commands.Context, song_number: int):
        """
        Elimina una canción de la lista de reproducción por su número en la cola
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if song_number <= 0 or song_number > self.playList.qsize():

                kizy.add_field(name="Error", value="Número de canción inválido.")
                return await ctx.send(embed=kizy)

            songs = [] # Extraer las canciones de la cola de reproducción
            for _ in range(self.playList.qsize()):
                ctx, song = await self.playList.get()
                songs.append((ctx, song))

            ctx, removed_song = songs.pop(song_number - 1) # Eliminar la canción especificada de la lista

            for song in songs: # Volver a poner las canciones restantes en la cola de reproducción
                self.playList.put_nowait(song)

            kizy.add_field(name="Canción retirada de la cola", value=f"*{removed_song.title}*", inline=False)
            kizy.add_field(name="", value=f"Espero no te hayas equivocado, y tampoco me eches la culpa.")
            kizy.set_thumbnail(url=removed_song.thumbnail)
            return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="leave", help="Abandona el canal de voz.")
    async def leave(self, ctx :commands.Context):
        """
        Se desconecta del canal de voz.
        """
        try:
            kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name="He salido del canal de voz", value="Me has desconectado. ¿En serio?")
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=kizy)
            await ctx.voice_client.disconnect()

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="queue", help="Muestra la lista de canciones.")
    async def queue(self, ctx :commands.Context):
        """
        Comprueba si la cola está vacía. Imprime la cantidad de canciones como haya en la lista.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if self.playList.qsize() <= 0:
                kizy.add_field(name="No hay más canciones en la cola", value="Parece ser que la lista esta vacía\n¿Por qué no añades un par?")
                return await ctx.send(embed=kizy)

            retval = ""
            for i in range(min(self.playList.qsize(), 20)):
                ctx, song = await self.playList.get() # Extraer la canción de la cola de reproducción
                self.playList.put_nowait((ctx, song))  # Devolver la canción a la cola de reproducción
                title = song.title if song.title else "No disponible" # Obtener el título de la canción
                retval += f"{i+1}. *{title}*\n" # Agregar el título a la lista de reproducción

            kizy.add_field(name="Tu lista de reproducción", value=f" {retval} ")
            return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="shuffle", help="Mezcla la lista de reproducción.")
    async def shuffle(self, ctx :commands.Context):
        """
        Si tiene 1 canción o menos, no hace la lista aleatoria.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if self.playList.qsize() <= 1:
                kizy.add_field(name="No puedo mezclar la lista si no la hay", value="Añade más de una canción para mezclar listas.")
                return await ctx.send(embed=kizy)

            songs = list(self.playList._queue)
            random.shuffle(songs)
            self.playList._queue.clear()
            for song in songs:
                self.playList.put_nowait(song)

            kizy.add_field(name="Lista mezclada", value="Siendo sincera ya no sé que canción sigue después de cual.")
            return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="loop", help="La reproducción actual entra en bucle.")
    async def loop(self, ctx :commands.Context, *args):
        """
        Si el autor está en el canal de voz y esta sonando, entonces entra en bucle la canción que este sonando.
        """
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await self.playList.join()  # Vacía la cola de reproducción
                kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
                kizy.add_field(name="Canción en bucle", value="¿Tu canción favorita? Estamos entrando en un bucleee. :woozy_face:")
                kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
                return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="lyrics", help="Muestra las letras de una canción buscada.")
    async def lyrics(self, ctx :commands.Context, *, song):
        """
        Muestra las letras de una canción buscada.
        """
        kizy = discord.Embed(color=discord.Color.blue(), timestamp=datetime.now())
        try:
            response = requests.get(f"https://api.lyrics.ovh/v1/{song}")
            if response.status_code == 200:
                lyrics_data = response.json() # Extraemos las letras de la respuesta JSON
                kizy.add_field(name="", value=lyrics_data["lyrics"])
            else:
                kizy.add_field(name="No pude encontrar las letras de la canción.", value="¡Intenta de nuevo con un título diferente!")

            await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="clear", help="Limpia la lista de canciones.")
    async def clear(self, ctx :commands.Context):
        """
        Limpia la lista de canciones.
        """
        try:
            if ctx.voice_client and ctx.voice_client.is_playing():
                self.playList :asyncio.Queue  = asyncio.Queue()
                kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
                kizy.add_field(name="Se ha detenido la reproducción", value="¡Oh no! ¿Te has cansado de mi? :(")
                kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
                return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="volume", help="Permite cambiar el volumen.")
    async def volume(self, ctx :commands.Context, volume: float):
        """
        Si el volumen es mayor de 100 o menor de 0, no permite cambiar el volumen.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if volume > 200:
                kizy.add_field(name="Volumen demasiado alto", value="No quiero que te quedes sordo.")
                return await ctx.send(embed=kizy)
            if volume < 0:
                kizy.add_field(name="Volumen demasiado bajo", value="O quizá solo quieres hacerme callar")
                return await ctx.send(embed=kizy)
            
            data :dict = readDB()
            data[str(ctx.guild.id)]["volume"] = volume / 100
            writeDB(data)

            ctx.voice_client.source.volume = volume / 100
            kizy.add_field(name="Se ha actualizado el volumen de la reproducción", value=f"Puse el volumen al {volume}%, ¡Disfruta!")
            return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

    @join.before_invoke
    @play.before_invoke
    @resume.before_invoke
    async def ensure_voice(self, ctx :commands.Context):
        """
        Si el autor esta en un canal, se une, si no, mostrará un mensaje de error.
        """
        try:
            if ctx.voice_client is None:
                if ctx.author.voice:
                    await ctx.author.voice.channel.connect()
                else:
                    kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
                    kizy.add_field(name="No estas en un canal de voz", value="¿Donde estas...? No te veo... 🥹🥺")
                    kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
                    return await ctx.send(embed=kizy)
                    # """ raise commands.CommandError("Author not connected to a voice channel.") """
            # elif ctx.voice_client.is_playing():
            #     return ctx.voice_client.stop()

        except Exception as e:
            print(e)

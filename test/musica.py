import aiohttp
import discord; from discord.ext import commands
import spotipy; from spotipy.oauth2 import SpotifyClientCredentials
import yt_dlp
from datetime import datetime
import asyncio
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

yt_dlp.utils.bug_reports_message = lambda: ""

ytdl_format_options = {
    "format": "bestaudio/best", 
    "outtmpl": "%(extractor)s-%(id)s-%(title)s.%(ext)s", 
    "restrictfilenames": True, 
    "noplaylist": False, 
    "nocheckcertificate": True, 
    "ignoreerrors": False, 
    "logtostderr": False, 
    "quiet": True, 
    "no_warnings": True, 
    "default_search": "auto", 
    "source_address": "0.0.0.0", 
    "extractaudio": True, 
    "audioformat": "mp3", 
    "preferredquality": "192", 
    "cookiefile": "cookies.txt", 
}

ffmpeg_options = {
    "options": "-vn", 
    "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", 
} 

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

# ===== Clase ========================================================================================== #

class YTDLSource(discord.PCMVolumeTransformer):
    """ Documentacion """
    def __init__(self, source, *, data :dict, volume :float = 0.1) -> None:
        super().__init__(source, volume)

        self.data :dict = data
        self.title = data.get("title")
        self.url = data.get("url")

# ===== Método ================================ #

    @classmethod
    async def from_url(cls, url:str, loop=None, stream :bool = False):
        """ Documentacion """
        """ spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()) """
        loop = loop or asyncio.get_event_loop()
        """ results = spotify.search(q=url, limit=1, type='track')
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_url = track['preview_url']

            if track_url:
               
                return cls(discord.FFmpegPCMAudio(track_url, **ffmpeg_options)) """

        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        with open("files/extract_info.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        if "entries" in data:
            data = data["entries"][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

# ===== Clase ========================================================================================== #

class Music(commands.Cog):
    """ Documentacion """
    def __init__(self, client) -> None:
        self.client :discord.Client = client
        self.playList :asyncio.Queue = asyncio.Queue()

# ===== Comando =============================== #

    @commands.command(name="play", aliases=["p"], help="Reproduce una canción.")
    async def play(self, ctx:commands.Context, *, link :str = ""):
        """ Documentacion """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        if link == "":
            return

        if link.startswith("https://open.spotify.com"):
            return
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()

        song = await YTDLSource.from_url(url=link, loop=self.client.loop, stream=True)
        await self.playList.put((ctx, song))

        if ctx.voice_client.is_playing():
            kizy.add_field(name="Se ha añadido a la cola:", value=song.title, inline=False)
            return await ctx.send(embed=kizy)

        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await self.nextSong(ctx)

    async def nextSong(self, ctx :commands.Context):
        """ Documentacion """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        if self.playList.empty():
            return

        ctx.voice_client.stop()
        ctx, song = await self.playList.get()
        ctx.voice_client.play(song, after=lambda: asyncio.run_coroutine_threadsafe(self.nextSong(ctx), self.client.loop))

        kizy = discord.Embed(title="**Ahora suena**",color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name="**Título**:",value=f"{song.title}",inline=False)
        await ctx.send(embed=kizy)

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
async def main() -> None:
    """ Documentacion """
    async with bot:
        await bot.add_cog(Music(bot))
        await bot.start("")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit(0)
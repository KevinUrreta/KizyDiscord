import discord; from discord.ext import commands
from datetime import datetime
from io import BytesIO
import aiohttp
import http
"""
Comando de Economía:
Implementa un sistema de economía en tu servidor donde los usuarios pueden ganar puntos participando en actividades.
"""
async def setup(client :commands.Bot):
    await client.add_cog(Fun(client))
# ===== Clase ========================================================================================== #

class Fun(commands.Cog):
    def __init__(self, client):
        self.client: discord.Client = client

# ===== Comando =============================== #

    async def randomimageapi(self, ctx: commands.Context,url: str, *endpoint: str) -> discord.Message:
        try:
            r = await http.get(url, res_method="json")
        except aiohttp.ClientConnectorError:
            return await ctx.send("The API seems to be down...")
        except aiohttp.ContentTypeError:
            return await ctx.send("The API returned an error or didn't return JSON...")

        result = r.response
        for step in endpoint:
            result = result[step]

        await ctx.send(result)

# ===== Comando =============================== #

    async def api_img_creator(self, ctx: commands.Context, url: str,filename: str, content: str = None) -> discord.Message:
        async with ctx.channel.typing():
            req = await http.get(url, res_method="read")

            if not req.response:
                return await ctx.send("I couldn't create the image ;-;")

            bio = BytesIO(req.response)
            bio.seek(0)
            return await ctx.send(content=content, file=discord.File(bio, filename=filename))

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def duck(self, ctx: commands.Context):
        """ Posts a random duck """
        await self.randomimageapi(ctx, "https://random-d.uk/api/v1/random", "url")

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def coffee(self, ctx: commands.Context):
        """ Posts a random coffee """
        await self.randomimageapi(ctx, "https://coffee.alexflipnote.dev/random.json", "file")

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def birb(self, ctx: commands.Context):
        """ Posts a random birb """
        await self.randomimageapi(ctx, "https://api.alexflipnote.dev/birb", "file")

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def sadcat(self, ctx: commands.Context):
        """ Post a random sadcat """
        await self.randomimageapi(ctx, "https://api.alexflipnote.dev/sadcat", "file")

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def cat(self, ctx: commands.Context):
        """ Posts a random cat """
        await self.randomimageapi(ctx, "https://api.alexflipnote.dev/cats", "file")

# ===== Comando =============================== #

    @commands.command()
    @commands.cooldown(rate=1, per=1.5, type=commands.BucketType.user)
    async def dog(self, ctx: commands.Context):
        """ Posts a random dog """
        await self.randomimageapi(ctx, "https://api.alexflipnote.dev/dogs", "file")


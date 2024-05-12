import discord; from discord.ext import commands
from datetime import datetime
import requests

async def setup(client :commands.Bot):
    await client.add_cog(Action(client))

url :str = 'https://api.waifu.pics'
sfw :tuple = {
    'waifu', 'neko', 'shinobu', 'megumin', 'bully', 'cuddle', 'cry', 'hug',
    'awoo', 'kiss', 'lick', 'pat', 'smug', 'bonk', 'yeet', 'blush',
    'smile', 'wave', 'highfive', 'handhold', 'nom', 'bite', 'glomp', 'pegar',
    'kill', 'kik', 'happy', 'wink', 'poke', 'dance', 'cringe'
}
nsfw :tuple = {'waifu', 'neko', 'trap', 'blowjob'}

# def main(lista :list):
#     sortedList = sorted(set(lista))
#     with open("commands/Action.py", "a") as file:
#         for i in sortedList:
#             file.write(f"""
# # ===== Comando =============================== #

#     @commands.command(name="{i}", help="")
#     async def {i}(self, ctx :commands.Context):
#         await self.gif(ctx, action="{i}", mensaje="")
# """)

# if __name__ == "__main__":
#     try:
#         main(lista=sfw)
#     except KeyboardInterrupt:
#         exit()

# ===== Clase ========================================================================================== #

class Action(commands.Cog):
    def __init__(self, client :discord.Client) -> None:
        self.client :discord.Client = client

    async def gif(self, ctx :commands.Context, action :str = None, mensaje :str = None):
        """
        Hace una búsqueda en la API de `anime`y devuelve \n
        la acción solicitada por el usuario.\n
        Enlaces de imagenes:
         - https://docs.waifu.im
         - https://api.waifu.pics
         - https://documentation.nekos.pro
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        kizy.add_field(name="", value=mensaje)

        if action is None: return None
        if action in sfw: category :str = "sfw"
        elif action in nsfw: category :str = "nsfw"
        try:
            response = requests.get(f"{url}/{category}/{action}") # Corregir?
            if response.status_code != 200: return
            kizy.set_image(url=response.json()["url"])

            return await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="awoo", help="")
    async def awoo(self, ctx :commands.Context):
        await self.gif(ctx, action="awoo", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="bite", help="")
    async def bite(self, ctx :commands.Context):
        await self.gif(ctx, action="bite", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="blowjob", help="")
    async def blowjob(self, ctx :commands.Context):
        if not ctx.channel.is_nsfw():
            return False
        await self.gif(ctx, action="blowjob", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="blush", help="")
    async def blush(self, ctx :commands.Context):
        await self.gif(ctx, action="blush", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="bonk", help="")
    async def bonk(self, ctx :commands.Context):
        await self.gif(ctx, action="bonk", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="bully", help="")
    async def bully(self, ctx :commands.Context):
        await self.gif(ctx, action="bully", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="cringewaifu", help="")
    async def cringewaifu(self, ctx :commands.Context):
        await self.gif(ctx, action="cringewaifu", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="cry", help="")
    async def cry(self, ctx :commands.Context):
        await self.gif(ctx, action="cry", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="cuddle", help="")
    async def cuddle(self, ctx :commands.Context):
        await self.gif(ctx, action="cuddle", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="dance", help="")
    async def dance(self, ctx :commands.Context):
        await self.gif(ctx, action="dance", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="glomp", help="")
    async def glomp(self, ctx :commands.Context):
        await self.gif(ctx, action="glomp", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="handhold", help="")
    async def handhold(self, ctx :commands.Context):
        await self.gif(ctx, action="handhold", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="happy", help="")
    async def happy(self, ctx :commands.Context):
        await self.gif(ctx, action="happy", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="highfive", help="")
    async def highfive(self, ctx :commands.Context):
        await self.gif(ctx, action="highfive", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="hug", help="")
    async def hug(self, ctx :commands.Context):
        await self.gif(ctx, action="hug", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="kickbutt", help="")
    async def kickbutt(self, ctx :commands.Context):
        await self.gif(ctx, action="kick", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="kill", help="")
    async def kill(self, ctx :commands.Context):
        await self.gif(ctx, action="kill", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="kiss", help="")
    async def kiss(self, ctx :commands.Context):
        await self.gif(ctx, action="kiss", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="lick", help="")
    async def lick(self, ctx :commands.Context):
        await self.gif(ctx, action="lick", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="megumin", help="")
    async def megumin(self, ctx :commands.Context):
        await self.gif(ctx, action="megumin", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="neko", help="")
    async def neko(self, ctx :commands.Context):
        await self.gif(ctx, action="neko", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="nom", help="")
    async def nom(self, ctx :commands.Context):
        await self.gif(ctx, action="nom", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="pat", help="")
    async def pat(self, ctx :commands.Context):
        await self.gif(ctx, action="pat", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="pegar", help="")
    async def pegar(self, ctx :commands.Context):
        await self.gif(ctx, action="pegar", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="poke", help="")
    async def poke(self, ctx :commands.Context):
        await self.gif(ctx, action="poke", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="shinobu", help="")
    async def shinobu(self, ctx :commands.Context):
        await self.gif(ctx, action="shinobu", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="smile", help="")
    async def smile(self, ctx :commands.Context):
        await self.gif(ctx, action="smile", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="smug", help="")
    async def smug(self, ctx :commands.Context):
        await self.gif(ctx, action="smug", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="trap", help="")
    async def trap(self, ctx :commands.Context):
        await self.gif(ctx, action="trap", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="waifu", help="")
    async def waifu(self, ctx :commands.Context):
        await self.gif(ctx, action="waifu", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="wave", help="")
    async def wave(self, ctx :commands.Context):
        await self.gif(ctx, action="wave", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="wink", help="")
    async def wink(self, ctx :commands.Context):
        await self.gif(ctx, action="wink", mensaje="")

# ===== Comando =============================== #

    @commands.command(name="yeet", help="")
    async def yeet(self, ctx :commands.Context):
        await self.gif(ctx, action="yeet", mensaje="")

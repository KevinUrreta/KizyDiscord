import discord; from discord.ext import commands
from datetime import datetime

async def setup(client :commands.Bot):
    await client.add_cog(Conf(client))

# ===== Clase ========================================================================================== #

class Conf(commands.Cog):
    def __init__(self, client :discord.Client) -> None:
        super().__init__()
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command(help="")
    async def conf(self, ctx :commands.Context):
        """ Documentacion """

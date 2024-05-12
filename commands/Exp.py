import discord; from discord.ext import commands

async def setup(client :commands.Bot):
    await client.add_cog(Exp(client))

# ===== Clase ========================================================================================== #

class Exp(commands.Cog):
    """ Documentacion """
    def __init__(self, client :discord.Client) -> None:
        super().__init__()
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command()
    async def exp(self, ctx :commands.Context):
        """ Documentacion """

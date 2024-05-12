import discord; from discord.ext import commands
import logging; import json; import os

manejo = logging.basicConfig(filename='files/registro.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
token :str = 'token'

def getPrefix(self, ctx :commands.Context):
    """ Obtiene el prefijo del servidor de un archivo JSON. """
    with open('files/configuracion.json', 'r') as f:
        data :list = json.load(f)
    return data[str(ctx.guild.id)]['prefix']

class App(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=getPrefix, intents=discord.Intents.all())

    async def on_ready(client):
        """ Carga otros comandos para no sobrecargar a Kizy. """
        for i in os.listdir('./commands'):
            if i.endswith('.py'):
                try:
                    await client.load_extension(f'commands.{i[:-3]}')
                except Exception as e:
                    print(e)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='tus llantos 😢'))

if __name__ == '__main__':
    KizY = App()
    try:
        KizY.run(token, log_handler=manejo)

    except KeyboardInterrupt:
        KizY.close()

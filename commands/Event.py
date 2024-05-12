import discord; from discord.ext import commands
from datetime import datetime
import json

async def setup(client :commands.Bot) -> None:
    await client.add_cog(Event(client))

def readDB():
    """ Abre un archivo en modo lectura. """
    try: 
        with open("files/configuracion.json", "r", encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return {}

def writeDB(save):
    """ Abre un archivo en modo escritura """
    with open("files/configuracion.json", "w", encoding="utf-8") as f: json.dump(save, f, indent=4)

# ===== Clase ========================================================================================== #

class Event(commands.Cog):
    """ Configuracion predeterminado para servidores. """
    def __init__(self, client :discord.Client) -> None:
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command(help="")
    async def welcome(self, ctx :commands.Context, channel :discord.TextChannel):
        """ Documentacion """
        data = readDB()
        data[str(ctx.guild.id)]["channels"] = {
            "welcome": channel.id
        }

# ===== Comando =============================== #

    @commands.command(help="")
    async def farewell(self, ctx :commands.Context, channel :discord.TextChannel):
        """ Documentacion """
        data = readDB()
        data[str(ctx.guild.id)]["channels"] = {
            "farewell": channel.id
        }

# ===== Welcome screen =============================== #

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """ Panel de bienvenida """
        try:
            channel = member.guild.system_channel
            if channel is not None:
                kizy = discord.Embed(
                    title=f"Bienvenido a {member.guild.name}!",
                    description=f"Esperamos que disfrutes tu estadía, {member.mention}!",
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await channel.send(embed=kizy)
        except Exception as e:
            print(f"Error en on_member_join: {e}")

# ===== Goodbye screen =============================== #

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """ Panel de despedida """
        try:
            channel = member.guild.system_channel
            if channel is not None:
                kizy = discord.Embed(
                    title="Adiós!",
                    description=f"{member.name} se ha ido de {member.guild.name}. Esperamos volver a verte pronto.",
                    color=discord.Color.red(),
                    timestamp=datetime.now()
                )
                await channel.send(embed=kizy)
        except Exception as e:
            print(f"Error en on_member_remove: {e}")

# ===== Write on files/configuracion.json =============================== #

    @commands.Cog.listener()
    async def on_guild_join(self, guild :discord.Guild,):
        """ Crea un registro de datos al unirse al servidor. """
        try:
            data :dict = readDB()
            if guild.id in data:
                return
            data[guild.id] = {
                    "servername": guild.name,
                    "prefix": "!",
                    "warned": [],
                    "muted": [],
                    "timeouted": [],
                    "kicked": [],
                    "banned": [],
                    "volume": 0.1
                }
            writeDB(data)
        except Exception as e:
            print(f"Error in on_guild_join: {e}")

# ===== Write on files/configuracion.json =============================== #

    @commands.Cog.listener()
    async def on_guild_remove(self, guild :discord.Guild):
        """ Elimina el registro al ser expulsado del servidor. """
        try:
            data :dict = readDB()
            if guild.id not in data:
                return
            data.pop(str(guild.id))
            writeDB(data)
        except Exception as e:
            print(f"Error in on_guild_remove: {e}")

# ===== Error handling =============================== #

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        """ Mensajes de error """
        import traceback # Se imprime la excepción
        traceback.print_exc()
        owner = self.client.get_user(self.client.owner_id) # Se envía un mensaje de error al usuario
        await owner.send(f"Ha ocurrido un error en el evento {event}: {args[0]}")
        print(f"on_error: {kwargs}")

# ===== Error handling =============================== #

    @commands.Cog.listener()
    async def on_command_error(self, ctx :commands.Context, error):
        """ Mensajes de error """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name="Por favor, notifica este error al desarrollador.", value=str(
            "La intención es solucionar los errores y mejorar mi rendimiento."
            f"Puedes usar {ctx.prefix}suggestion, describiendo el problema."),
            inline=False
        )
        kizy.set_footer(text=f"Contacta con el desarrollador {ctx.author.display_name}.", icon_url=ctx.author.avatar)
        error_messages :dict = {
            commands.MissingRequiredArgument: "MissingRequiredArgument",
            commands.BadArgument: "BadArgument",
            commands.CommandOnCooldown: "CommandOnCooldown",
            commands.DisabledCommand: "DisabledCommand",
            commands.NoPrivateMessage: "NoPrivateMessage",
            commands.CheckFailure: "CheckFailure",
            commands.CommandInvokeError: "CommandInvokeError",
        }
        for error_type, error_name in error_messages.items():
            if isinstance(error, (error_type)):
                kizy.add_field(name=error_name, value=error, inline=False)
        if commands.CommandNotFound: raise ("No existe este comando")
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(f"on_command_error: {e}")

# ===== Comando =============================== #
# setrole, setchannel, lock, unlock
# Comando de generación de gráficos o diagramas: Crea gráficos estadísticos o diagramas a partir de datos proporcionados.
# Comando de cálculo de tiempo de entrega de paquetes: Consulta el estado y el tiempo estimado de entrega de paquetes utilizando servicios de seguimiento de envíos en línea.
# Comando de búsqueda de tutoriales de programación: Encuentra tutoriales y recursos educativos para aprender diferentes lenguajes de programación y tecnologías.

    @commands.command(name="setchannel")
    @commands.has_permissions(administrator=True)
    async def setchannel(self, ctx :commands.Context, channel_type: str, channel: discord.TextChannel):
        """
        Establece un canal predeterminado para un tipo específico de mensaje.

        Args:
            channel_type (str): El tipo de mensaje para el cual establecer el canal (por ejemplo, "welcome", "farewell").
            channel (discord.TextChannel): El canal al que se redirigirán los mensajes.

        Ejemplo:
            !setchannel welcome #bienvenida
        """
        if channel_type.lower() not in self.default_channels:
            return await ctx.send("Tipo de canal no válido. Los tipos válidos son: welcome, farewell")

        self.default_channels[channel_type.lower()] = channel.id
        await ctx.send(f"Canal predeterminado para {channel_type.lower()} establecido en {channel.mention}.")

# ===== Comando =============================== #

    @commands.command()
    async def snipe(self, ctx, num_messages: int = 1):
        channel = ctx.channel
        if channel.id not in self.deleted_messages:
            await ctx.send("No hay mensajes eliminados en este canal.")
            return

        deleted_message = self.deleted_messages[channel.id]
        author = deleted_message.author
        content = deleted_message.content

        await ctx.send(f"**Mensaje eliminado por {author}**: {content}")

        if num_messages > 1:
            for i in range(1, min(num_messages, len(self.deleted_messages[channel.id]))):
                deleted_message = self.deleted_messages[channel.id][i]
                author = deleted_message.author
                content = deleted_message.content
                await ctx.send(f"**Mensaje eliminado por {author}**: {content}")

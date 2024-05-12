import discord; from discord.ext import commands
from datetime import datetime
import platform
import json

async def setup(client :commands.Bot):
    client.remove_command("help")
    await client.add_cog(Info(client))

def readDB():
    """ Abre un archivo en modo lectura. """
    try: 
        with open("files/configuracion.json", "r", encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return {}

def writeDB(save):
    """ Abre un archivo en modo escritura """
    with open("files/configuracion.json", "w", encoding="utf-8") as f: json.dump(save, f, indent=4)

# ===== Clase ========================================================================================== #

class Info(commands.Cog):
    """
    Comandos que muestan información al usuario que lo solicite.
    """
    def __init__(self, client :discord.Client) -> None:
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command(name="avatar", help="Muestra el avatar de un miembro.")
    async def avatar(self, ctx :commands.Context, member :discord.Member):
        """
        Muestra el avatar de un miembro.
        """
        member = member or ctx.author
        try:
            kizy = discord.Embed(color=discord.Color.purple())
            kizy.add_field(name=f"Avatar de {member.display_name}", value=f"**Enlace:**\n{member.avatar.url}")
            kizy.set_image(url=member.avatar)
            await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="ayuda", help="Muestra la lista de comandos disponibles.")
    async def ayuda(self, ctx :commands.Context):
        """
        Muestra la lista de comandos disponibles.
        """
        commands = [ # Obtener la lista de comandos disponibles
            (command.name, command.help or "No hay ayuda disponible")
            for command in self.client.commands
        ]

        chunks = [commands[i:i+25] for i in range(0, len(commands), 25)] # Dividir la lista de comandos en grupos de 25 o menos

        for index, chunk in enumerate(chunks): # Enviar un embed por cada grupo de comandos
            embed = discord.Embed(title=f"Lista de Comandos ({index+1}/{len(chunks)})", color=discord.Color.purple(), timestamp=datetime.now())
            for command_name, command_help in chunk:
                embed.add_field(name=f"`{command_name}`", value=command_help, inline=True)
            try:
                await ctx.send(embed=embed)
            except Exception as e:
                print(e)

# ===== Comando =============================== #

    @commands.command(name="banner", help="Muestra el banner de un miembro.")
    async def banner(self, ctx :commands.Context, member :discord.Member):
        """
        Muestra el banner de un usuario.
        """
        member = member or ctx.author
        try:
            kizy = discord.Embed(color=discord.Color.purple())
            kizy.add_field(name=f"Avatar de {member.display_name}", value=f"**Enlace:**\n{member.banner.url}")
            kizy.set_image(url=member.banner)
            await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command()
    async def cluster(self, ctx :commands.Context):
        """
        Comando para mostrar información del nodo y cluster.
        """
        try:
            system = platform.uname()
            kizy = discord.Embed(title="Información del Cluster", color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name="Sistema Operativo", value=system.system)
            kizy.add_field(name="Nombre del Nodo", value=platform.node())
            kizy.add_field(name="Versión de Python", value=platform.python_version())
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    # @commands.command()
    # async def donate(self, ctx :commands.Context):
    #     """
    #     Comando para proporcionar información de donación.
    #     """
    #     try:
    #         kizy = discord.Embed(color=discord.Color.purple())
    #         kizy.add_field(name="", value="Aún no implementado.")
    #         return await ctx.send(embed=kizy)

    #     except Exception as e:
    #         kizy = discord.Embed(color=discord.Color.purple()).add_field(
    #             name="Ha surgido un error, por favor contacta con `@KevinUrreta`",
    #             value=f"` {e}  `"
    #         ); return await ctx.send(embed=kizy)

# ===== Comando =============================== #

    # @commands.command()
    # async def help(self, ctx :commands.Context):
    #     """
    #     Comando para mostrar la lista de comandos disponibles.
    #     """
    #     try:
    #         kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
    #         help_msg = "Lista de comandos disponibles:\n\n"
    #         for command in self.client.commands:
    #             help_msg += f"{ctx.prefix}{command.name} {command.signature}\n"
            
    #         kizy.add_field(name="", value=help_msg) # Crea y envía el mensaje de ayuda en un embed
    #         return await ctx.send(embed=kizy)

    #     except Exception as e:
    #         print(e)

    @commands.command(help="Muestra una lista de comandos disponibles o información detallada sobre un comando específico.")
    async def help(self, ctx: commands.Context, command_name: str = None):
        """Muestra una lista de comandos disponibles o información detallada sobre un comando específico."""
        if command_name:
            command = self.bot.get_command(command_name)
            if command:
                embed = discord.Embed(title=f"Ayuda: {command_name}", description=command.help, color=ctx.author.color)
                await ctx.send(embed=embed)
            else:
                await ctx.send("Ese comando no existe.")
        else:
            embed = discord.Embed(title="Lista de comandos", description="Aquí tienes una lista de comandos disponibles:", color=ctx.author.color)
            for command in self.bot.commands:
                embed.add_field(name=command.name, value=command.help or "Sin descripción.", inline=False)
            await ctx.send(embed=embed)


# ===== Comando =============================== #

    # @commands.command(name="invite", help="Obtiene el enlace de invitación del bot.")
    # async def invite(self, ctx :commands.Context):
    #     """
    #     Obtiene el enlace de invitación del bot.
    #     """
    #     invite_link = discord.utils.oauth_url(self.client.user.id, permissions=discord.Permissions.all())
    #     kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
    #     kizy.add_field(name="Enlace de invitación")
    #     await ctx.send(f"Aquí está el enlace de invitación para añadirme a tu servidor: {invite_link}")


# ===== Comando =============================== #

    # @commands.command()
    # async def partners(self, ctx :commands.Context):
    #     """
    #     Comando para mostrar las comunidades más fieles.
    #     """
    #     try:
    #         kizy = discord.Embed(color=discord.Color.purple())
    #         kizy.add_field(name="", value="Aún no implementado.")
    #         return await ctx.send(embed=kizy)

    #     except Exception as e:
    #         kizy = discord.Embed(color=discord.Color.purple()).add_field(
    #             name="Ha surgido un error, por favor contacta con `@KevinUrreta`",
    #             value=f"` {e}  `"
    #         ); return await ctx.send(embed=kizy)

# ===== Comando =============================== #

    @commands.command(name="ping", help="Muesta la latencia.")
    async def ping(self, ctx :commands.Context):
        """
        Comprueba la latencia de Kizy.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_author(name=ctx.me.name, icon_url=ctx.me.avatar)
        kizy.add_field(name="", value=str(
            "🏓 Ping!\n"
            f"📨 Mensajes: {round(self.client.latency * 1000)}ms\n"
            f"🍡 Shard : {round(ctx.bot.latency * 1000)}ms"
            ))
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="serverinfo", help="Muestra información general del servidor.")
    async def serverinfo(self, ctx: commands.Context) -> None:
        """
        Muestra información general del servidor.
        """
        roles = [role.name for role in ctx.guild.roles]
        num_roles = len(roles)
        if num_roles > 50:
            roles = roles[:50]
            roles.append(f">>>> Mostrando [50/{num_roles}] Roles")
        roles = ", ".join(roles)

        kizy = discord.Embed(title="**Servidor:**", description=f"`{ctx.guild}`", color=discord.Color.purple(), timestamp=datetime.now())
        if ctx.guild.icon is not None:
            kizy.set_thumbnail(url=ctx.guild.icon.url)
        kizy.add_field(name="Server ID", value=ctx.guild.id)
        kizy.add_field(name="Miembros", value=ctx.guild.member_count)
        kizy.add_field(name="Canales", value=f"{len(ctx.guild.channels)}")
        kizy.add_field(name=f"Roles ({len(ctx.guild.roles)})", value=roles)
        kizy.set_footer(text=f"Creado en: {ctx.guild.created_at.strftime('%Y-%m-%d, %H:%M:%S')}")
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="setprefix", help="Cambia el prefijo del servidor")
    async def setprefix(self, ctx :commands.Context, prefix: str = "!"):
        """
        Comando para cambiar el prefijo del servidor.
        """
        data = readDB()
        data[str(ctx.guild.id)]["prefix"] = prefix
        writeDB(data)
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name="Se ha cambiado el prefijo", value=f"Ahora puedes usar ` {prefix} ` para ejecutar comandos.")
        try:
            return await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="start", help="Mensaje de como configurar el bot.")
    async def start(self, ctx :commands.Context):
        """
        Devuelve un mensaje de ayuda para la configuración inicial
        del bot dentro del servidor, de todas las posibles opciones.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        kizy.set_thumbnail(url=ctx.me.avatar)
        kizy.set_author(
            name="Desarrollada por @KevinUrreta",
            url="https://github.com/KevinUrreta",
            icon_url="https://cdn.discordapp.com/avatars/501448786925846559/eb0f009e965ed9d27b2f48758e3f5cc5.png?size=1024"
        )
        kizy.add_field(name=f"Configuración inicial de {ctx.me.name}", value=str(
            "¡Hola! Soy Kizy 👋, tu compañera en Discord.\n"
            "🎵 Puedo ayudarte con música, moderación"
            "y comandos divertidos."
            "¡Únete y descubre todo lo que puedo hacer! 🚀"
            ),
            inline=False
        )
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command()
    async def updates(self, ctx :commands.Context):
        """
        Comando para mostrar la lista de actualizaciones del bot.
        """
        kizy = discord.Embed(color=discord.Color.purple())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            with open("files/actualizaciones.md", "r", encoding="utf-8") as updates:
                update = updates.read()
                kizy.add_field(name="Actualizaciones:", value=update)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    # @commands.command()
    # async def vote(self, ctx :commands.Context):
    #     """
    #     Comando para votar por Kizy.
    #     """
    #     try:
    #         kizy = discord.Embed(color=discord.Color.purple())
    #         kizy.add_field(name="", value="Aún no implementado.")
    #         return await ctx.send(embed=kizy)

    #     except Exception as e:
    #         kizy = discord.Embed(color=discord.Color.purple()).add_field(
    #             name="Ha surgido un error, por favor contacta con `@KevinUrreta`",
    #             value=f"` {e}  `"
    #         ); return await ctx.send(embed=kizy)

# ===== Comando =============================== #

    @commands.command(name="userinfo", help="Muestra la información general de un miembro.")
    async def userinfo(self, ctx :commands.Context, member : discord.Member):
        """
        Muestra la información general de un miembro.
        """
        member = member or ctx.author
        kizy = discord.Embed(title="Información de Usuario", color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.add_field(name="Rol más alto", value=member.top_role, inline=True)
        kizy.add_field(name="Se unió al servidor", value=member.joined_at.strftime("%Y-%m-%d %H:%M:%S"), inline=False)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

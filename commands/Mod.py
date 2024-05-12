import discord; from discord.ext import commands
from datetime import datetime
import json
from discord import app_commands


async def setup(client :commands.Bot):
    await client.add_cog(Mod(client))

def readDB():
    """ Abre un archivo en modo lectura. """
    try:
        with open("files/configuracion.json", "r", encoding="utf-8") as f: return json.load(f)
    except FileNotFoundError: return {}

def writeDB(save):
    """ Abre un archivo en modo escritura """
    with open("files/configuracion.json", "w", encoding="utf-8") as f: json.dump(save, f, indent=4)

# ===== Clase ========================================================================================== #

class Mod(commands.Cog):
    """
    Comandos básicos de moderación para un servidor.
    """
    def __init__(self, client :discord.Client) -> None:
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command(help="Elimina un número de mensajes.")
    async def cls(self, ctx :commands.Context, *, limit :int = 1):
        """
        Permite al usuario limpiar una cantidad de mensajes en el servidor.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if limit < 1:
                kizy.add_field(name="¿Número negativo?", value=f"¿Pretendes que borre {limit} mensajes?")
                return await ctx.send(embed=kizy, delete_after=3)

            await ctx.channel.purge(limit=limit + 1)
            kizy.add_field(name=f"Se han borrado {limit} mensajes", value="Ahh, así mejor, esta más limpio...")
            return await ctx.send(embed=kizy, delete_after=3)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(ban_members=True)
    @commands.command(help="Banea a un usuario del servidor adjuntando un motivo.")
    async def ban(self, ctx :commands.Context, member: discord.Member, *, reason :str = "Sin razón."):
        """
        Banea a un usuario del servidor adjuntando un motivo.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            await member.ban(reason=reason)
            kizy.add_field(name=f"{member.mention} ha sido baneado por:", value=reason)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(help="Añade un rol a un usuario.")
    async def addrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        """
        Añade un rol a un usuario
        """
        await member.add_roles(role)
        await ctx.send(f"Se ha añadido el rol {role.name} a {member.mention}.")

# ===== Comando =============================== #

    @commands.command(help="Quita un rol de un usuario.")
    async def removerole(self, ctx: commands.Context, member: discord.Member, role: discord.Role):
        """
        Quita un rol de un usuario
        """
        await member.remove_roles(role)
        await ctx.send(f"Se ha eliminado el rol {role.name} de {member.mention}.")

# ===== Comando =============================== #

    @commands.command(help="Crea un nuevo rol en el servidor.")
    async def createrole(self, ctx: commands.Context, *, role_name: str):
        """
        Crea un nuevo rol en el servidor
        """
        guild = ctx.guild
        role = await guild.create_role(name=role_name)
        await ctx.send(f"Se ha creado el rol {role.mention}.")

# ===== Comando =============================== #

    @commands.command(help="Elimina un rol del servidor.")
    async def deleterole(self, ctx: commands.Context, role: discord.Role):
        """
        Elimina un rol del servidor
        """
        await role.delete()
        await ctx.send(f"Se ha eliminado el rol {role.name}.")

# ===== Comando =============================== #

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Expulsa a un usuario del servidor adjuntando un motivo.")
    async def kick(self, ctx :commands.Context, member: discord.Member, *, reason :str = "Sin razón."):
        """
        Expulsa a un usuario del servidor adjuntando un motivo.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            await member.kick(reason=reason)
            kizy.add_field(name=f"{member.mention} ha sido expulsado por:", value=reason)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Establece un \"timeout\" a un usuario de forma temporal.")
    async def timeout(self, ctx :commands.Context, member: discord.Member, duration: int = 1, *, reason :str = "Sin razón."):
        """
        Establece un "timeout" a un usuario de forma temporal.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            data :dict = readDB()
            timestamp = datetime.now().strftime("%Y-%m-%d")
            if str(member.id) not in data:
                data[str(member.id)] = {
                    "servername": ctx.guild.name,
                    "prefix": "!",
                    "warned": {},
                    "muted": {},
                    "timeouted": {str(ctx.author.id): timestamp},
                    "volume": 0.5
                }
            else:
                data[str(member.id)]["timeouted"][str(ctx.author.id)] = timestamp

            writeDB(data)
            await ctx.send(f"{member.mention} ha sido silenciado por {duration} minutos.")
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Advierte a un usuario, adjuntado un motivo.")
    async def warn(self, ctx :commands.Context, member: discord.Member, reason :str = "Sin razón."):
        """
        Advierte a un usuario, adjuntado un motivo.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            data = readDB()
            if str(member.id) not in data:
                data[str(member.id)] = {
                    "servername": ctx.guild.name,
                    "prefix": "!",
                    "warned": {str(member.id): 1},
                    "muted": {},
                    "timeouted": {},
                    "volume": 0.5
                }
            else:
                if str(member.id) not in data[str(member.id)]["warned"]:
                    data[str(member.id)]["warned"][str(member.id)] = 1
                else:
                    data[str(member.id)]["warned"][str(member.id)] += 1

                if data[str(member.id)]["warned"][str(member.id)] >= 3:
                    kizy.add_field(name="Tiene 3 o más advertencias", value=f"Creo que deberiamos de banearlo.")
                    return await ctx.send(embed=kizy)
            writeDB(data)
        
            kizy.add_field(name="", value=f"{member.mention} ha sido advertido por {reason}.")
            await ctx.send(embed=kizy) # Aquí puedes agregar más acciones, como enviar un mensaje privado al usuario advertido
        
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(change_nickname=True)
    @commands.command(aliases=["setnick"], pass_context=True, no_pm=True)
    async def setnickname(self, ctx :commands.Context, *, member :discord.Member, txt :str = None):
        """
        Cambia el apodo de un usuario del servidor, dejar vacío para quitar apodo.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            await member.edit(nick=txt)  # Cambiar el apodo del usuario
            kizy.add_field(name="", value=f"Cambiado el apodo a: `{txt}`")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(ban_members=True)
    @commands.command(help="Retira el ban de un usuario.")
    async def unban(self, ctx :commands.Context, member: discord.Member):
        """
        Retira el ban de un usuario.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            banned_users = await ctx.guild.bans()
            for ban_entry in banned_users:
                user = ban_entry.user
                if user == member:
                    await ctx.guild.unban(user)
                    kizy.add_field(name="", value=f"Sanción eliminada para {user.mention}.")
                    return await ctx.send(embed=kizy)
            kizy.add_field(name="", value=f"{member.mention} no estaba en la lista de baneados.")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Retira el timeout establecido al usuario.")
    async def untimeout(self, ctx :commands.Context, member: discord.Member):
        """
        Retira el timeout establecido al usuario.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            data = readDB()
            if str(member.id) in data:
                if str(ctx.author.id) in data[str(member.id)]["timeouted"]:
                    del data[str(member.id)]["timeouted"][str(ctx.author.id)]

                writeDB(data)
                kizy.add_field(name="", value=f"Se levantó el tiempo de silencio de {member.mention}.")
            else:
                kizy.add_field(name="", value=f"{member.mention} no está silenciado.")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.has_permissions(kick_members=True)
    @commands.command(help="Retira la advertencia a un usuario.")
    async def unwarn(self, ctx :commands.Context, member: discord.Member):
        """
        Retira la advertencia a un usuario.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_thumbnail(url=member.avatar)
        kizy.add_field(name="Nombre", value=member.name, inline=True)
        kizy.add_field(name="Apodo", value=member.nick, inline=True)
        kizy.add_field(name="ID", value=member.id, inline=True)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            data = readDB()
            if str(member.id) in data:
                if str(ctx.author.id) in data[str(member.id)]["warned"]:
                    data[str(member.id)]["warned"][str(ctx.author.id)] -= 1
                    if data[str(member.id)]["warned"][str(ctx.author.id)] <= 0:
                        del data[str(member.id)]["warned"][str(ctx.author.id)]

                writeDB(data)
                kizy.add_field(name="", value=f"Se eliminó una advertencia de {member.mention}.")
            else:
                kizy.add_field(name="", value=f"{member.mention} no tiene advertencias.")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

    # @commands.hybrid_group(
    #     name="warning",
    #     description="Manage warnings of a user on a server.",
    # )
    # @commands.has_permissions(manage_messages=True)
    # async def warning(self, context: discord.Context) -> None:
    #     """
    #     Manage warnings of a user on a server.

    #     :param context: The hybrid command context.
    #     """
    #     if context.invoked_subcommand is None:
    #         embed = discord.Embed(
    #             description="Please specify a subcommand.\n\n**Subcommands:**\n`add` - Add a warning to a user.\n`remove` - Remove a warning from a user.\n`list` - List all warnings of a user.",
    #             color=0xE02B2B,
    #         )
    #         await context.send(embed=embed)

    # @warning.command(name="add", description="Adds a warning to a user in the server.",)
    # @commands.has_permissions(manage_messages=True)
    # @app_commands.describe(
    #     user="The user that should be warned.",
    #     reason="The reason why the user should be warned.",
    # )
    # async def warning_add(self, context: discord.Context, user: discord.User, *, reason: str = "Not specified") -> None:
    #     """
    #     Warns a user in his private messages.

    #     :param context: The hybrid command context.
    #     :param user: The user that should be warned.
    #     :param reason: The reason for the warn. Default is "Not specified".
    #     """
    #     member = context.guild.get_member(user.id) or await context.guild.fetch_member(
    #         user.id
    #     )
    #     total = await self.bot.database.add_warn(
    #         user.id, context.guild.id, context.author.id, reason
    #     )
    #     embed = discord.Embed(
    #         description=f"**{member}** was warned by **{context.author}**!\nTotal warns for this user: {total}",
    #         color=0xBEBEFE,
    #     )
    #     embed.add_field(name="Reason:", value=reason)
    #     await context.send(embed=embed)
    #     try:
    #         await member.send(
    #             f"You were warned by **{context.author}** in **{context.guild.name}**!\nReason: {reason}"
    #         )
    #     except:
    #         # Couldn't send a message in the private messages of the user
    #         await context.send(
    #             f"{member.mention}, you were warned by **{context.author}**!\nReason: {reason}"
    #         )

    # @warning.command(name="remove", description="Removes a warning from a user in the server.")
    # @commands.has_permissions(manage_messages=True)
    # @app_commands.describe(
    #     user="The user that should get their warning removed.",
    #     warn_id="The ID of the warning that should be removed.",
    # )
    # async def warning_remove(self, context: discord.Context, user: discord.User, warn_id: int) -> None:
    #     """
    #     Warns a user in his private messages.

    #     :param context: The hybrid command context.
    #     :param user: The user that should get their warning removed.
    #     :param warn_id: The ID of the warning that should be removed.
    #     """
    #     member = context.guild.get_member(user.id) or await context.guild.fetch_member(
    #         user.id
    #     )
    #     total = await self.bot.database.remove_warn(warn_id, user.id, context.guild.id)
    #     embed = discord.Embed(
    #         description=f"I've removed the warning **#{warn_id}** from **{member}**!\nTotal warns for this user: {total}",
    #         color=0xBEBEFE,
    #     )
    #     await context.send(embed=embed)

    # @warning.command(name="list", description="Shows the warnings of a user in the server.")
    # @commands.has_guild_permissions(manage_messages=True)
    # @app_commands.describe(user="The user you want to get the warnings of.")
    # async def warning_list(self, context: discord.Context, user: discord.User) -> None:
    #     """
    #     Shows the warnings of a user in the server.

    #     :param context: The hybrid command context.
    #     :param user: The user you want to get the warnings of.
    #     """
    #     warnings_list = await self.bot.database.get_warnings(user.id, context.guild.id)
    #     embed = discord.Embed(title=f"Warnings of {user}", color=0xBEBEFE)
    #     description = ""
    #     if len(warnings_list) == 0:
    #         description = "This user has no warnings."
    #     else:
    #         for warning in warnings_list:
    #             description += f"• Warned by <@{warning[2]}>: **{warning[3]}** (<t:{warning[4]}>) - Warn ID #{warning[5]}\n"
    #     embed.description = description
    #     await context.send(embed=embed)

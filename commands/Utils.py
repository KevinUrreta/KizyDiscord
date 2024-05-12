import discord; from discord.ext import commands
from googletrans import Translator
from datetime import datetime
# from openai import OpenAI
import asyncio
import secrets
import string
import random
import base64
import socket
import pytz
import re

async def setup(client :commands.Bot):
    await client.add_cog(Utils(client))

# ===== Clase ========================================================================================== #

class Utils(commands.Cog):
    """
    Comandos posiblemente útiles para los usuarios de Discord.
    """
    def __init__(self, client :discord.Client) -> None:
        self.client :discord.Client = client

# ===== Comando =============================== #

    @commands.command(name="", help="Lanza una moneda y muestra si salió cara o cruz.")
    async def coinflip(self, ctx :commands.Context):
        """
        Lanza una moneda y muestra si salió cara o cruz.
        """
        moneda = random.choice(["Cara", "Cruz"])
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name=f"El resultado al lanzar la moneda es: {moneda}", value=f"¿Cara o cruz? Pues es {moneda}")
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="El bot elige entre las opciones propuestas por el usuario.")
    async def choose(self, ctx :commands.Context, *,args :str):
        """
        El bot elige entre las opciones propuestas por el usuario.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            argumentos :list = args.split(" ")
            if args is None:
                kizy.add_field(name="Faltan argumentos", value="¿Quieres que escoja entre nada y nada? Pues nada entonces.")
                return ctx.send(embed=kizy)
            if argumentos < 1:
                kizy.add_field(name="Faltan argumentos", value="Solo me estas dando una opción, es lo único que puedo escoger.")
                return ctx.send(embed=kizy)
            response = random.choice(argumentos)
            kizy.add_field(name="Eligiendo:", value=f"Mmm... Elijo: {response}")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(help="Cuenta las palabras y letras de un texto.")
    async def count(self, ctx :commands.Context, *, text :str = None):
        """ Documentacion """
        if text is None: return
        for palabra in text:
            texto :str = "".join(palabra)
        await ctx.send(texto)

# ===== Comando =============================== #

    @commands.command(name="", help="Codifica y decodifica texto en Base64.")
    async def base64(self, ctx: commands.Context, *, text :str = None):
        """
        Códifica y descodifica le mensaje del usuario.
        """
        texto_original = text.encode("utf-8") # Codificar y decodificar datos en Base64
        texto_codificado = base64.b64encode(texto_original).decode("utf-8")
        texto_decodificado = base64.b64decode(texto_codificado).decode("utf-8")

        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name="Texto original:", value=texto_decodificado, inline=False)
        kizy.add_field(name="Texto codificado:", value=texto_codificado, inline=False)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if text is None:
                kizy.add_field(name="Faltan argumentos", value="¿Quieres que escoja entre nada y nada? Pues nada entonces.")
                return ctx.send(embed=kizy)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Devuelve la fecha actual.")
    async def date(self, ctx :commands.Context):
        """
        Devuelve la fecha actual.
        """
        timezones = {
            "Londres": "Europe/London",
            "Nueva York": "America/New_York",
            "Los Ángeles": "America/Los_Angeles",
            "Tokio": "Asia/Tokyo",
        }
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        for city, timezone in timezones.items():
            time = datetime.now(pytz.timezone(timezone)).strftime("%Y-%m-%d %H:%M:%S")
            kizy.add_field(name=city, value=time, inline=True)
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Lanza un dado de Nº caras.")
    async def dice(self, ctx :commands.Context, caras :int = 6):
        """
        Tira un dado virtual y obtén un resultado totalmente aleatorio.
        """
        dado = random.randint(1, caras)
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name=f"El resultado al lanzado es: {dado}", value="Ohh, ¿Eso es bueno o es malo?")
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        kizy.set_thumbnail(url="https://clipartmag.com/image/dice-drawing-2.jpg")
        try:
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Realiza una búsqueda en Google.")
    async def search(self, ctx :commands.Context, *, consulta :str = None):
        """
        Busca información en Google.
        """
        link = f"https://www.google.com/search?q={consulta.replace(' ', '+')}&tbm=isch"
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name="Imágenes relacionadas:", value=link)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        kizy.set_image(url=link)
        try:
            if consulta is None:
                kizy.add_field(name="Faltan argumentos", value="¿Quieres que busque \"nada\".")
                return ctx.send(embed=kizy)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Pregunta a la IA cualquier duda.")
    async def gpt(self, ctx :commands.Context, *,args :str = None):
        """ 
        Pregunta a la IA cualquier duda.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.add_field(name=f"Lo sentimos aún no está implementado", value=f"Estamos trabajando para traer esta nueva función.")
        kizy.set_footer(text=f"Pedido por `{ctx.author.display_name}`", icon_url=ctx.author.avatar)
        kizy.set_thumbnail(url="https://static.vecteezy.com/system/resources/previews/024/558/807/large_2x/openai-chatgpt-logo-icon-free-png.png")
        try:
            if args is None:
                kizy.add_field(name="Faltan argumentos", value="¿Quieres que busque \"nada\".")
                return await ctx.send(embed=kizy)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    # @commands.command(name="facts", help="Proporciona un hecho aleatorio sobre un tema específico.")
    # async def facts(self, ctx :commands.Context, topic="chuck_norris"):
    #     """
    #     Proporciona un hecho aleatorio sobre un tema específico.
    #     Por defecto, se utiliza el tema de Chuck Norris.
    #     """
    #     try:
    #         response = requests.get(f"https://api.chucknorris.io/jokes/random?category={topic}")

    #         if response.status_code == 200:
    #             # Extraemos el hecho de la respuesta JSON
    #             fact_data = response.json()

    #             kizy = discord.Embed(title="Random facts", color=discord.Color.green())
    #             kizy.add_field(name=f"#{topic.capitalize()}", value=fact_data["value"], inline=False)

    #             await ctx.send(embed=kizy)
    #         else:
    #             await ctx.send("No pude encontrar un hecho en este momento. ¡Intenta de nuevo más tarde!")
    #     except Exception as e:
    #         print(e)
    #         await ctx.send("Ha ocurrido un error al obtener el hecho.")

# ===== Comando =============================== #

    # @commands.command(name="", help="Envía un chiste aleatorio.")
    # async def joke(self, ctx :commands.Context):
    #     """
    #     Envía un chiste aleatorio.
    #     """
    #     try:
    #         response = requests.get("https://official-joke-api.appspot.com/random_joke")

    #         if response.status_code == 200:
    #             # Extraemos el chiste de la respuesta JSON
    #             joke_data = response.json()

    #             # Construimos el mensaje embed con el chiste
    #             kizy = discord.Embed(title="Chiste", color=discord.Color.purple(), timestamp=datetime.now())
    #             kizy.add_field(name=joke_data["setup"], value=joke_data["punchline"], inline=False)
    #             await ctx.send(embed=kizy)
    #         else:
    #             kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
    #             kizy.add_field(name="No ha sido posible encontrar un chiste", value="Ay, lo siento no encuentro mi libro de chistes.")
    #             await ctx.send(embed=kizy)

    #     except Exception as e:
    #         print(e)
    #         await ctx.send("Ha ocurrido un error al obtener el chiste.")

# ===== Comando =============================== #

    @commands.command(name="", help="Realiza operaciones matemáticas.")
    async def math(self, ctx :commands.Context, *, args):
        """
        Realiza operaciones matemáticas. Recomendable tener cuidado, \n
        `eval()` puede ejecutar código en python y pueder revelar, \n
        dañar u otrasacciones maliciosas.
        """
        def is_valid_expression(args):
            """ Expresión regular para validar la expresión matemática. """
            pattern = re.compile(r"^[\d\s\+\-\*\/\(\)\.]+$")
            return bool(pattern.match(args))

        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if not is_valid_expression(args):
                kizy.add_field(name="", value="La expresión matemática es inválida.")
                return ctx.send(embed=kizy)

            resultado = eval(args) # Proteger, puede ejecutar código en python.
            kizy.add_field(name="Resultado:", value=f"{args} = {resultado}")
            return await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Realiza una consulta de DNS.")
    async def nslookup(self, ctx: commands.Context, *, domain):
        """
        Realiza una consulta de DNS (nslookup) para un dominio dado.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        kizy.set_thumbnail(url="https://static.bejbej.ca/app-icons/423175511-256x256.png")
        try:
            if domain is None:
                kizy.add_field(name="Faltan argumentos", value="No me has dado ni el nombre de dominio ni la dirección IP.")
                return ctx.send(embed=kizy)

            ip_address = socket.gethostbyname(domain) # Realizar la consulta DNS
            kizy.add_field(name=f"Nombre de dominio", value=domain)
            kizy.add_field(name=f"Dirección IP", value=ip_address)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Genera una contraseña aleatoria.")
    async def passwd(self, ctx :commands.Context, long :int = 10):
        """
        Genera una contraseña aleatoria, y se la envía al usuario por privado.
        """
        try:
            caracteres = string.ascii_letters + string.digits + string.punctuation
            contraseña = "".join(secrets.choice(caracteres) for _ in range(long))

            kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name=f"Contraseña generada", value=contraseña, inline=False)
            kizy.add_field(name=f"", value="Tranquilo, tú contraseña quedará entre tu y yo 7u7.")
            kizy.set_thumbnail(url="https://www.sethserver.com/images/random-password-generator-og.png")
            return await ctx.author.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Crea una encuesta en el canal donde se ejecuta el comando.")
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """
        Crea una encuesta en el canal donde se ejecuta el comando.
        """
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if question is None:
                kizy.add_field(name="No has definido la pregunta", value ="¿Y bueno, y la pregunta donde esta?")
                return await ctx.send(embed=kizy)

            if len(options) < 2 or len(options) > 8:
                if len(options) < 2:
                    kizy.add_field(name="No has definido las opciones", value ="Debes proporcionar al menos 2 opciones para la encuesta.")
                    return await ctx.send(embed=kizy)
                return

            formatted_options = [f"{index + 1}. {option}" for index, option in enumerate(options)]
            kizy = discord.Embed(title=f"Encuesta: {question}", description="\n".join(formatted_options), color=ctx.author.color)
            message = await ctx.send(embed=kizy)
            for emoji in ("🔵", "🟢", "🟡", "🟠", "🔴", "🟣", "🟤", "⚫️", "⚪️", "🟣"):
                await message.add_reaction(emoji)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(help="Crea un recordatorio para una fecha y hora específicas.")
    async def remindme(self, ctx: commands.Context, when: str, *, reminder: str):
        """Crea un recordatorio para una fecha y hora específicas."""
        try:
            remind_time = dateparser.parse(when) # type: ignore
            if remind_time:
                now = datetime.now()
                delta = remind_time - now
                if delta.total_seconds() <= 0:
                    await ctx.send("La fecha y hora proporcionadas ya han pasado.")
                else:
                    await asyncio.sleep(delta.total_seconds())
                    await ctx.send(f"Recordatorio para {ctx.author.mention}: {reminder}")
            else:
                await ctx.send("No pude entender la fecha y hora proporcionadas.")
        except Exception as e:
            await ctx.send(f"Ocurrió un error al programar el recordatorio: {e}")


# ===== Comando =============================== #

    @commands.command(name="", help="Da la vuelta a un mensaje.")
    async def reverse(self, ctx :commands.Context, *, mensaje:str = None):
        """
        Repite el mensaje de un usuario, devolviendolo del revés.
        """
        await ctx.channel.purge(limit=1)
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar)
        kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            if mensaje is None:
                kizy.add_field(name="No has proporcionado ningún mensaje.", value ="No puedo darle la vuelta si no me dices a que.")
                return await ctx.send(embed=kizy)
            if "enoyreve@" in mensaje:
                kizy.add_field(name="", value="Jasjs, buen intento, pero eri gai.", delete_after=5)
                return await ctx.send(embed=kizy)
            elif "ereh@" in mensaje:
                kizy.add_field(name="", value="Jasjs, buen intento, pero eri gai.", delete_after=5)
                return await ctx.send(embed=kizy)
            else:
                kizy.add_field(name="", value="{}".format(mensaje)[::-1])
                return await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Repite el mensaje del autor.")
    async def say(self, ctx :commands.Context, *, mensaje :str = None):
        """
        Repite el mensaje de un usuario, pero antes borra el mensaje del autor.
        """
        await ctx.channel.purge(limit=1)
        kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
        kizy.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar)
        # kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
        try:
            # if mensaje is None:
            #     kizy.add_field(name="No has proporcionado ningún mensaje.", value ="No puedo darle la vuelta si no me dices a que.")
            #     return await ctx.send(embed=kizy)
            if "@everyone" in mensaje: # Checking to make sure the user isn"t trying to ping everyone or here
                kizy.add_field(name="", value="Jasjs, buen intento, pero eri gai.")
                return await ctx.send(embed=kizy, delete_after=5)
            elif "@here" in mensaje:
                kizy.add_field(name="", value="Jasjs, buen intento, pero eri gai.")
                return await ctx.send(embed=kizy, delete_after=5)
            kizy.add_field(name="Mensaje:", value=mensaje)
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Envia comentarios o ideas al desarrollador.")
    async def suggestion(self, ctx :commands.Context, *, args):
        """
        Envia comentarios o ideas al desarrollador, esto se guarda en un archivo ".txt".
        """
        try:
            if args is None:
                kizy.add_field(name="No has sugerido nada", value ="No puedes sugerir nada.")
                return await ctx.send(embed=kizy)

            with open("files/sugerido.md", "a", encoding="utf-8") as file:
                file.write(str(
                    "<!-- COMENTARIO ABIERTO -->\n"
                    f"Nombre: {ctx.author.name}, apodo: {ctx.author.display_name}, id: {ctx.author.id}\n"
                    f"{args}\n"
                    "<!-- FIN DEL COMENTARIO -->"
                ))
            kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name="Enviado con éxito", value=f"Le he dejado al desarrollador lo que has sugerido.", inline=False)
            kizy.add_field(name="", value=f"`{args}`", inline=False)
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            await ctx.send(embed=kizy)

        except Exception as e:
            print(e)

# ===== Comando =============================== #

    @commands.command(name="", help="Traduce un mensaje a otro idioma.")
    async def translate(self, ctx :commands.Context, *, args):
        """
        Traduce un mensaje a otro idioma.
        """
        try:
            translate = Translator()
            if args is None:
                kizy.add_field(name="No puedo traducir", value ="¿Traduzco nada?")
                return await ctx.send(embed=kizy)
            detect_lang:str = translate.detect(args).lang
            tranlatedText = translate.translate(args, dest="es").text
            kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
            kizy.add_field(name=f"Traducido de  {detect_lang.upper()}", value=tranlatedText)
            kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
            kizy.set_thumbnail(url="https://is1-ssl.mzstatic.com/image/pf/us/r30/Purple1/v4/5c/3b/8f/5c3b8f24-90e6-e8b4-3a42-05357bf5c2f1/mzl.pimgpiek.png")
            await ctx.send(embed=kizy)
        except Exception as e:
            print(e)

# ===== Comando =============================== #

    # @commands.command(name="", help="Obtén datos del clima.")
    # async def weather(self, ctx :commands.Context):
    #     """
    #     Obtén datos del clima según tu zona.
    #     """
    #     kizy = discord.Embed(color=discord.Color.purple(), timestamp=datetime.now())
    #     kizy.add_field(name="", value="")
    #     kizy.set_footer(text=f"Pedido por: {ctx.author.display_name}", icon_url=ctx.author.avatar)
    #     try:
    #         await ctx.send(embed=kizy)
    #     except Exception:
    #         return
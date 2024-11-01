import asyncio
import os
from dotenv import load_dotenv

from PIL import Image

# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands

from html2image import Html2Image

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = None
DISCORD_WELCOME_CHANNEL = None
STATUS = os.getenv("STATUS")

ENVIRONMENT = os.getenv("ENV")

if ENVIRONMENT.casefold() == "DEV".casefold():
    DISCORD_GUILD_ID = 700439581706682428
    DISCORD_WELCOME_CHANNEL = 813158607155757157
elif ENVIRONMENT.casefold() == "PROD".casefold():
    DISCORD_GUILD_ID = 1264408428697096284
    DISCORD_WELCOME_CHANNEL = 1264408430677065799


COMPUTER_OS = os.getenv("OS")

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(intents=intents, command_prefix="=")


@bot.event
async def on_ready():
    if STATUS.casefold() == "MAINT".casefold():
        await bot.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game(name="Maintenance miaou"))
    else:
        await bot.change_presence(activity=discord.Game(name="Made with <3 by Babibelbleu"))
    print(f"Ready | alphav1 ")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        await ctx.send(f"Une erreur inconnue est survenue : {error}")


@bot.event
async def on_member_join(member: discord.Member):
    channel = bot.get_channel(DISCORD_WELCOME_CHANNEL)
    hti = Html2Image(size=(1800, 620))

    if COMPUTER_OS.casefold() == "UNIX".casefold():
        hti.browser.flags = ["--no-sandbox", "--hide-scrollbars"]

    with open("member_join.html") as f:
        file_content = f.read()
        file_content = file_content.replace("{NICKNAME}", member.name) \
            .replace("{AVATAR_LINK}", member.avatar.url)

        new_file = open(f"{member.id}_card.html", "w")
        new_file.write(file_content)
        new_file.close()

    hti.screenshot(html_file=f"{member.id}_card.html",
                   css_file="style_member_join.css",
                   save_as='page.png')

    #Remove white bakcground (linux)
    img = Image.open("page.png")
    img = img.convert("RGBA")

    datas = img.getdata()

    new_data = []

    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 254:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save("./page_linux.png", "PNG")

    await asyncio.sleep(delay=0)
    await channel.send(
        content=f"❤-------------------❤---------------------❤---------------------❤-------------------❤\nWOOOOOO "
                f"{member.mention} vient de rejoindre  🌸Le Panier Rose🌸 Bienvenue a toi ! ^^\n"
                f"N'oublie surtout pas d'aller lire et d'accepter les <#1264593405883846718> pour avoir accès au reste "
                f"du serveur, c'est super important !\n**Nous te souhaitons un bon séjour parmi nous ! ^^ 💖**",
        file=discord.File("page_linux.png")
    )
    os.remove(f"{member.id}_card.html")
    os.remove("page.png")
    os.remove("page_linux.png")


@bot.hybrid_command(name="simulate_member_join", description="Simule l'évent on_member_join")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221, 1264408428931977220)
async def simulate_member_join(ctx: commands.Context, member: discord.Member):
    await ctx.defer()
    await asyncio.sleep(1)
    await on_member_join(member)
    await ctx.interaction.response.send_message("c'est bon", ephemeral=True)


@bot.hybrid_command(name="sync", description="Synchronise les commandes avec l'arbre courant.")
@commands.has_any_role("membre IUT", 1264408428931977223, 1264408428931977221, 1264408428931977220)
async def sync(ctx: commands.Context):
    bot.tree.copy_global_to(guild=discord.Object(id=DISCORD_GUILD_ID))
    await bot.tree.sync(guild=discord.Object(id=DISCORD_GUILD_ID))
    await ctx.send("Commandes synchronisées")


@bot.hybrid_command()
async def ping(ctx: commands.Context):
    await ctx.typing()
    await asyncio.sleep(1)
    await ctx.send("Miaou ! :cat:")

bot.run(DISCORD_BOT_TOKEN)

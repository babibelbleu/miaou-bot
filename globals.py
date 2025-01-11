import os
from dotenv import load_dotenv

# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord.ext import commands

# import util functions
from utils import get_dict_from_json_file

load_dotenv()

# Discord related
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_GUILD_ID = None
DISCORD_WELCOME_CHANNEL = None

_intents = discord.Intents.all()
_intents.message_content = True
bot = commands.Bot(intents=_intents, command_prefix="=")

# other vars
STATUS = os.getenv("STATUS")
ENVIRONMENT = os.getenv("ENV")
COMPUTER_OS = os.getenv("OS")

# depending on the environment, we chose specific channels and guilds
if ENVIRONMENT.casefold() == "DEV".casefold():
    DISCORD_GUILD_ID = 700439581706682428
    DISCORD_WELCOME_CHANNEL = 813158607155757157
    DISCORD_ROLE_REACT_CHANNEL = 1327293915291848804
    DISCORD_RULES_CHANNEL = 813175916141608990
    DISCORD_MEMBER_ROLE = "membre IUT"
elif ENVIRONMENT.casefold() == "PROD".casefold():
    DISCORD_GUILD_ID = 1264408428697096284
    DISCORD_WELCOME_CHANNEL = 1264408430677065799
    DISCORD_RULES_CHANNEL = 1264593405883846718
    DISCORD_MEMBER_ROLE = "🌱Membre"

# strings
strings = get_dict_from_json_file("strings.json")

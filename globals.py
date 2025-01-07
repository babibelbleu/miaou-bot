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

# strings
strings = get_dict_from_json_file("strings.json")
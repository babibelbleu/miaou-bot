from enum import Enum
import discord


class LogLevel(Enum):
    INFO = discord.Color.dark_teal(),
    DEBUG = discord.Color.teal(),
    ERROR = discord.Color.dark_magenta(),
    WARNING = discord.Color.dark_red()

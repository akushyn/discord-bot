import os
import discord
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PRIVILEGED_USERS = os.getenv('PRIVILEGED_USERS')
PRIVILEGED_USERS = PRIVILEGED_USERS.split(',')


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)


def check_nickname_change(before, after):
    """
    Checks if a member's nickname has been changed to a privileged user.
    Returns True if the nickname has been changed, False otherwise.
    """
    if before.nick != after.nick:
        if after.nick is not None and after.nick.lower() in PRIVILEGED_USERS:
            return True
    return False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_update(before, after):
    if check_nickname_change(before, after):
        await after.kick(reason="Nickname changed to a privileged user")


@bot.event
async def on_member_join(member):
    if member.nick is not None and member.nick.lower() in PRIVILEGED_USERS:
        await member.kick(reason="Nickname set to a privileged user on join")


bot.run(DISCORD_TOKEN)

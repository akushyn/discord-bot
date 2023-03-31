import discord
from discord.ext import commands
import config


def get_privileged_roles():
    """
    Get parsed privileged roles
    :return: List of privileged roles
    """
    return [u.strip() for u in config.PRIVILEGED_USER_ROLES.split(',')]


intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)


def is_privileged_nick(nick):
    """
    Check whether member nick equal to one of privileged roles
    :param nick: Member nickname
    :return: Returns True if the nickname equal to privileged roles, False otherwise.
    """
    if nick is not None and nick.lower() in get_privileged_roles():
        return True
    return False


def check_nickname_change(before, after):
    """
    Checks if a member's nickname has been changed to a privileged user.
    :param before: Member before
    :param after: Member after
    :return: Returns True if the nickname has been changed, False otherwise.
    """
    if before.nick != after.nick:
        if is_privileged_nick(after.nick):
            return True
    return False


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_member_update(before, after):
    if check_nickname_change(before, after):
        await after.kick(reason=config.MEMBER_UPDATE_KICK_REASON)


@bot.event
async def on_member_join(member):
    if is_privileged_nick(member.nick):
        await member.kick(reason=config.MEMBER_JOIN_KICK_REASON)


bot.run(config.DISCORD_TOKEN)

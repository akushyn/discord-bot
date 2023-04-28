import discord
import config
from logger import logger
from utils import parse_privileged_roles, get_privileged_members, get_discord_server, kick_duplicate, log_message

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# parse privileged roles
privileged_roles = parse_privileged_roles()
privileged_members = []
log_channel = None

# Set up the background task to run check_for_duplicates once a day
from discord.ext import tasks  # noqa


@tasks.loop(seconds=config.MEMBER_CHECK_PERIOD)
async def daily_update_privileged_members():
    """
    Periodic task to update list of privileged members
    """
    global privileged_members

    server = get_discord_server(client, server_id=config.DISCORD_SERVER_ID)
    updated_privileged_members = await get_privileged_members(server, roles=privileged_roles)

    # there are changes to privileged members list
    if set(privileged_members) != set(updated_privileged_members):
        # update privileged members list
        privileged_members = updated_privileged_members

        # log changes to channel
        member_names = [m.display_name for m in privileged_members]
        await log_message(f"Updated privileged members: {member_names}", channel=log_channel)


@client.event
async def on_ready():
    """
    Bot initialization event
    """
    global log_channel
    log_channel = client.get_channel(config.DISCORD_CHANNEL_ID)  # Get the channel object using its ID

    # start periodic task to update privileged members
    daily_update_privileged_members.start()
    await log_message('Bot is ready.', channel=log_channel)
    await log_message(f'Manage privileged roles: {privileged_roles}', channel=log_channel)


@client.event
async def on_member_join(member):
    """
    Member join event
    :param member: Member try to join
    """
    logger.info("MEMBER JOIN EVENT")
    await kick_duplicate(member=member, privileged_members=privileged_members, channel=log_channel)


@client.event
async def on_member_update(before, after):
    """
    Member update event
    :param before: Member before update
    :param after: Member after update
    """

    logger.info("MEMBER UPDATE EVENT")
    if before.display_name != after.display_name or before.nick != after.nick or before.name != after.name:
        await kick_duplicate(member=after, privileged_members=privileged_members, channel=log_channel)


client.run(config.DISCORD_TOKEN)

import discord
import config
from logger import logger
from utils import get_token_ratio, parse_privileged_roles

intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# parse privileged roles
privileged_roles = parse_privileged_roles()
privileged_members = []


async def get_privileged_members():
    """
    Get privileged members, i.e members with one of privileged roles
    :return:
    """
    return [m for m in client.get_all_members() if any(role.name in privileged_roles for role in m.roles)]


async def check_for_duplicate(member):
    """
    Check Member `nick`, `name`, `display_name` for the duplication with existing privileged members
    :param member: Join member
    """

    logger.info(f"Privileged roles: {privileged_roles}")

    members = [m for m in privileged_members if any(role.name in privileged_roles for role in m.roles)]
    # logger.info(f"Privileged members: {members}")

    logger.info(f"Verify member with ID={member.id}")
    logger.info(f"\t\tdisplay_name={member.display_name}")
    logger.info(f"\t\tname={member.name}")
    logger.info(f"\t\tnick={member.nick}")

    for m in members:

        if m == member:
            continue

        if member.display_name and get_token_ratio(member.display_name, m.display_name) >= config.MATCH_TOKEN_RATIO:
            logger.info(f"Kicking member {member.display_name} "
                        f"due to reason: {config.MEMBER_DISPLAY_NAME_DUPLICATE_REASON}")
            await member.kick(reason=config.MEMBER_DISPLAY_NAME_DUPLICATE_REASON)
        elif member.name and get_token_ratio(member.name, m.name) >= config.MATCH_TOKEN_RATIO:
            logger.info(f"Kicking member {member.display_name} "
                        f"due to reason: {config.MEMBER_NAME_DUPLICATE_REASON}")
            await member.kick(reason=config.MEMBER_NAME_DUPLICATE_REASON)
        elif member.nick and get_token_ratio(member.nick, m.nick) >= config.MATCH_TOKEN_RATIO:
            logger.info(f"Kicking member {member.display_name} "
                        f"due to reason: {config.MEMBER_NICK_DUPLICATE_REASON}")
            await member.kick(reason=config.MEMBER_NICK_DUPLICATE_REASON)


# Set up the background task to run check_for_duplicates once a day
from discord.ext import tasks  # noqa


@tasks.loop(seconds=config.MEMBER_CHECK_PERIOD)  # set loop to run once a day
async def daily_update_privileged_members():
    global privileged_members
    privileged_members = await get_privileged_members()
    print(privileged_members)


@client.event
async def on_ready():
    # start periodic task to update privileged members
    daily_update_privileged_members.start()
    print('Bot is ready.')


@client.event
async def on_member_join(member):
    """
    Member join event
    :param member: Member try to join
    """
    logger.info("MEMBER JOIN EVENT")
    await check_for_duplicate(member=member)


@client.event
async def on_member_update(before, after):
    """
    Member update event
    :param before: Member before update
    :param after: Member after update
    """

    logger.info("MEMBER UPDATE EVENT")
    if before.display_name != after.display_name or before.nick != after.nick or before.name != after.name:
        await check_for_duplicate(member=after)

client.run(config.DISCORD_TOKEN)

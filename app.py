import discord
import config
from logger import logger
from utils import get_token_ratio


def parse_privileged_roles():
    """
    Get parsed privileged roles
    :return: List of privileged roles
    """
    return [u.strip() for u in config.PRIVILEGED_USER_ROLES.split(',')]


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

# parse privileged roles
privileged_roles = parse_privileged_roles()


@client.event
async def on_member_join(member):
    """
    Member join event
    :param member: Member try to join
    """
    logger.info("MEMBER JOIN EVENT")
    await check_for_duplicate(member)


@client.event
async def on_member_update(before, after):
    """
    Member update event
    :param before: Member before update
    :param after: Member after update
    """

    logger.info("MEMBER UPDATE EVENT")
    if before.display_name != after.display_name or before.nick != after.nick or before.name != after.name:
        await check_for_duplicate(after)


async def check_for_duplicate(member):
    """
    Check Member `nick`, `name`, `display_name` for the duplication with existing privileged members
    :param member: Join member
    """

    logger.info(f"Privileged roles: {privileged_roles}")

    members = [m for m in member.guild.members if any(role.name in privileged_roles for role in m.roles)]
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


client.run(config.DISCORD_TOKEN)

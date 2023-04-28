from fuzzywuzzy import fuzz

import config
from logger import logger


def get_token_ratio(s1, s2):
    """
    Get token ratio between two strings
    """
    if s1 is None or s2 is None:
        ratio = 0
    elif s1 == s2:
        ratio = 100
    else:
        ratio = fuzz.token_set_ratio(s1, s2)

    return ratio


def parse_privileged_roles():
    """
    Get parsed privileged roles
    :return: List of privileged roles
    """
    return [u.strip() for u in config.PRIVILEGED_USER_ROLES.split(',')]


def get_discord_server(client, server_id=config.DISCORD_SERVER_ID):
    """
    Get server object by server ID
    :param client: Discord client
    :param server_id: ID of server
    :return: Discord server object
    """
    servers = [guild for guild in client.guilds if guild.id == server_id]
    if servers:
        return servers[0]

    return None


async def get_privileged_members(server, roles):
    """
    Get privileged members, i.e members with one of privileged roles
    :param server: Discord server
    :param roles: A list of privileged role names

    :return: List of Member objects
    """
    return [m for m in server.members if any(role.name in roles for role in m.roles)]


async def get_duplicate_reason(member, privileged_members, logger=None):
    """
    Get duplication reason.
    Duplication checks by:
        - nick
        - name
        - display_name

    :param member: Member object we verify for duplicate
    :param privileged_members: A list of members with privileged roles
    :param logger: Logger
    """

    # logger.info(f"Privileged roles: {privileged_roles}")

    logger.info(f"Verify member with ID={member.id}")
    logger.info(f"\t\tdisplay_name={member.display_name}")
    logger.info(f"\t\tname={member.name}")
    logger.info(f"\t\tnick={member.nick}")

    reason = None
    for m in privileged_members:
        if member.display_name and get_token_ratio(member.display_name, m.display_name) >= config.MATCH_TOKEN_RATIO:
            # reason = f"Kicking member due to reason: {config.MEMBER_DISPLAY_NAME_DUPLICATE_REASON}"
            # await member.kick(reason=config.MEMBER_DISPLAY_NAME_DUPLICATE_REASON)
            reason = config.MEMBER_DISPLAY_NAME_DUPLICATE_REASON
            break
        elif member.name and get_token_ratio(member.name, m.name) >= config.MATCH_TOKEN_RATIO:
            # logger.info(f"Kicking member {member.display_name} "
            #             f"due to reason: {config.MEMBER_NAME_DUPLICATE_REASON}")
            # await member.kick(reason=config.MEMBER_NAME_DUPLICATE_REASON)
            reason = config.MEMBER_NAME_DUPLICATE_REASON
            break
        elif member.nick and get_token_ratio(member.nick, m.nick) >= config.MATCH_TOKEN_RATIO:
            # logger.info(f"Kicking member {member.display_name} "
            #             f"due to reason: {config.MEMBER_NICK_DUPLICATE_REASON}")
            # await member.kick(reason=config.MEMBER_NICK_DUPLICATE_REASON)
            reason = config.MEMBER_NICK_DUPLICATE_REASON
            break

    return reason


async def kick_duplicate(member, privileged_members, channel=None):
    """
    Kick member. Log reason to discord channel
    :param member:
    :param privileged_members:
    :param channel:
    :return:
    """
    reason = await get_duplicate_reason(member, privileged_members, logger)

    if reason:
        await member.kick(reason=reason)

        await log_message(
            message=f"Kicking member due to reason: {reason}",
            channel=channel
        )


async def log_message(message, channel=None):
    logger.info(message)

    if channel:
        await channel.send(message)

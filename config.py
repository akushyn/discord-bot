import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PRIVILEGED_USER_ROLES = os.getenv('PRIVILEGED_USER_ROLES')

MEMBER_UPDATE_KICK_REASON = "Nickname changed to a privileged user"
MEMBER_JOIN_KICK_REASON = "Nickname set to a privileged user on join"

# how many % changed nickname should match with roles
MATCH_TOKEN_RATIO = 100

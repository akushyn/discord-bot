import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PRIVILEGED_USER_ROLES = os.getenv('PRIVILEGED_USER_ROLES')

MEMBER_NICK_DUPLICATE_REASON = "Member 'nickname' changed to a privileged user"
MEMBER_NAME_DUPLICATE_REASON = "Name changed to a privileged user"
MEMBER_DISPLAY_NAME_DUPLICATE_REASON = "Display Name changed to a privileged user"

# how many % changed nickname should match with roles
MATCH_TOKEN_RATIO = 100

# discord server ID
DISCORD_SERVER_ID = os.getenv('DISCORD_SERVER_ID')

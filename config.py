import os

from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
PRIVILEGED_USER_ROLES = os.getenv('PRIVILEGED_USER_ROLES')

MEMBER_NICK_DUPLICATE_REASON = "Member used 'nickname' of a privileged user"
MEMBER_NAME_DUPLICATE_REASON = "Member used 'name' of a privileged user"
MEMBER_DISPLAY_NAME_DUPLICATE_REASON = "Member used 'display_name' of a privileged user"

# duration in seconds to check members
MEMBER_CHECK_PERIOD = 60*60*24
# how many % changed nickname should match with roles
MATCH_TOKEN_RATIO = 100

# discord server ID
DISCORD_SERVER_ID = int(os.getenv('DISCORD_SERVER_ID')) if os.getenv('DISCORD_SERVER_ID') else None
DISCORD_CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID')) if os.getenv('DISCORD_CHANNEL_ID') else None

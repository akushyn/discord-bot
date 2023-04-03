# discord-bot

### Installation

Clone the repository
```
git clone https://github.com/akushyn/discord-bot.git
```

Create & activate venv

```
cd discord-bot
python3 -m venv venv
source venv/bin/activate
```

Install dependencies
```
pip3 install -r requirements.txt
```

Create `.env` file from `env.example`
```
cp env.example .env
```

### Run the discord bot

Ensure you python script is running. 
```
python3 app.py
```

#### How to install discord bot:

1. Create a new application on the Discord Developer Portal: Go to https://discord.com/developers/applications and create a new application. Give it a name and a profile picture.

2. Create a bot user for your application: In the application settings, navigate to the "Bot" section and click "Add Bot". Give your bot a name and profile picture.

3. Get your bot's token: In the bot settings, click the "Copy" button next to the token field. Keep this token secret, as it is essentially the password for your bot.

4. Invite your bot to your Discord server: In the bot settings, navigate to the "OAuth2" section and select the "bot" scope. Select the permissions your bot will need, and copy the generated URL. Open this URL in your web browser and select the server you want to add your bot to.

#### How to get the server ID:

1. Open Discord and navigate to the server you want to retrieve the ID for.
2. Right-click on the server name in the left-hand sidebar and select "Server Settings" from the context menu.
3. In the Server Settings page, select the "Widget" tab.
4. Look for the "Server ID" field and copy the ID number that is displayed.
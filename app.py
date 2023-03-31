import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="-", intents=intents)


client = discord.Client()


async def check_nickname_change(member):
    privileged_roles = ["Admin", "Moderator"] # Change this to the roles you want to check for
    for role in member.roles:
        if role.name in privileged_roles and member.nick is not None and role.name not in member.nick:
            await member.kick(reason="Changed nickname to privileged user")
            break


@client.event
async def on_member_update(before, after):
    if before.nick != after.nick:
        await check_nickname_change(after)


@client.event
async def on_member_join(member):
    await check_nickname_change(member)


client.run("TOKEN")
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!hello'):
        await message.channel.send('My Name is akushyn!!!')


bot.run(DISCORD_TOKEN)
print('success')

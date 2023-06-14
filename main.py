from os import environ

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
SERVER_ID = environ.get('SERVER_ID')

intents = discord.Intents.default()
intents.message_content = True

# client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='$', intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$kursant'):
        member = message.author
        # server = client.get_guild(SERVER_ID)
        # member = await server.fetch_member(message.author.id)
        role = discord.utils.get(member.guild.roles, name='Test1')
        # print(server)
        # print(role.is_bot_managed())
        # print(type(role))
        await member.add_roles(role)
        # print(role.members)
        # role.members.append(member)
        # print(role.members)
        # await message.channel.send(f'{member.name}, {member.roles}, {role}')

    if message.content.startswith('$bot'):
        member = message.author
        role = discord.utils.get(member.guild.roles, name='Administrator')
        print(role.permissions, role.members)
        print('-' * 10)

client.run(DISCORD_TOKEN)
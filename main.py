from os import environ, path
import logging
import csv

import discord
from discord.ext import commands

from dotenv import load_dotenv

from utils import generate_token


ROLES = {
    'pystart': 'Test1',
    'pyrest': 'Test2',
}

logging.basicConfig(level=logging.INFO, filename='DoKoduBot_test.log', encoding='utf8', format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
load_dotenv()
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')

intents = discord.Intents.all()

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.command(name='kursant')
async def add_trainee(message):
    member = message.author
    logging.info(f'Start adding new trainee - {member.name}')
    role = discord.utils.get(member.guild.roles, name='Test1')
    await member.add_roles(role)
    await member.send(f'Teraz już masz nową rolę - {role.name}')
    logging.info(f'Adding complete\nMember: {member}\nRole: {role.name}')


@client.command(name='generate_codes')
@commands.has_permissions(administrator=True)
async def generate_codes(message, course, counter:int = 1):
    logging.info(f'generate {counter} new codes by {message.author.name}')
    for i in range(counter):
        if not path.exists('codes.csv'):
            with open('codes.csv', mode='w', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['token', 'course', 'used', 'used_date', 'used_by',])
        with open('codes.csv', mode='a', encoding='utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [generate_token(), course, False, None, None,]
            )

client.run(DISCORD_TOKEN)

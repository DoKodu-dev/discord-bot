'''
Bot to manage discord server - can add roles by using token.

All commands are written in Polish because bot is used on Polish discord server.
All operations are logging into "DoKoduBot_test.log.txt"
'''
from os import environ
import json
import logging

import discord
from discord.ext import commands

from dotenv import load_dotenv

from database.database import Database
from utils import generate_token

#pylint: disable=logging-fstring-interpolation

with open('roles.json', encoding='utf8') as json_file:
    ROLES = json.load(json_file)

load_dotenv()

DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
LOG_FILENAME = environ.get('LOG_FILENAME', 'DoKoduBot_test.log')

logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME, encoding='utf8',
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

database = Database()

intents = discord.Intents.all()

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    ''' Starting info '''
    logging.info(f'We have logged in as {client.user}')


@client.command(name='kursant')
async def add_trainee(message, token=None):
    ''' Add role for user using token.
    After complete the adding role process bot send PM to user and inform her/him

    Arguments:
        message -- command name
        token -- token to add specific role
    '''
    if token is not None:
        member = message.author
        row_from_db = database.get_token(token)

        if row_from_db is not None and not row_from_db[3]:
            role_name, course_channel_id = ROLES.get(row_from_db[2])

            logging.info(f'Start adding new trainee - {member.name}')
            role = discord.utils.get(member.guild.roles, name=role_name)
            channel = client.get_channel(int(course_channel_id))
            used_token = database.use_token(token, member.name)
            if used_token is not None:
                await member.add_roles(role)
                await member.send(f'Teraz już masz nową rolę - {role.name}')
                logging.info(
                    f'Adding complete | Member: {member} | Role: {role.name}')
                await channel.send(f'<@{member.id}>, witaj na pokładzie :)')


@client.command(name='generate_codes')
@commands.has_permissions(administrator=True)
async def generate_codes(message, course, counter: int = 1):
    ''' Prepare tokens to send to users

    Arguments:
        message -- command name
        course -- name of course for which you need tokens - courses are symbolic names of roles

    Keyword Arguments:
        counter -- how many tokens you want to prepare? (default: {1})
    '''
    logging.info(f'generate {counter} new codes by {message.author.name}')

    tokens = []

    while len(tokens) < counter:
        new_token = generate_token()
        token = database.save_token(new_token, course)
        if token:
            tokens.append(new_token)

    tokens = '\n'.join(tokens)
    await message.author.send(f'Wygenerowałeś tokeny dla kursu {course}:\n{tokens}')

try:
    client.run(DISCORD_TOKEN)
finally:
    database.connection.close()

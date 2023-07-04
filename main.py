'''
Bot to manage discord server - can add roles by using token.

All commands are written in Polish because bot is used on Polish discord server.
All operations are logging into "DoKoduBot_test.log.txt"
'''
from os import environ, path
import logging
import csv

import discord
from discord.ext import commands

from dotenv import load_dotenv

from utils import generate_token, get_role_by_token_from_csv


ROLES = {
    'pystart': 'Test1',
    'pyrest': 'Test2',
}

load_dotenv()
DISCORD_TOKEN = environ.get('DISCORD_TOKEN')
LOG_FILENAME = environ.get('LOG_FILENAME', 'DoKoduBot_test.log')

logging.basicConfig(level=logging.INFO, filename=LOG_FILENAME, encoding='utf8',
                    format='%(asctime)s [%(levelname)s]: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')

intents = discord.Intents.all()

client = commands.Bot(command_prefix='$', intents=intents)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


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
        course = get_role_by_token_from_csv(token, './codes.csv')
        role_name = ROLES.get(course)
        if role_name is not None:
            logging.info(f'Start adding new trainee - {member.name}')
            role = discord.utils.get(member.guild.roles, name=role_name)
            await member.add_roles(role)
            await member.send(f'Teraz już masz nową rolę - {role.name}')
            logging.info(
                f'Adding complete | Member: {member} | Role: {role.name}')


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
    for i in range(counter):
        if not path.exists('codes.csv'):
            with open('codes.csv', mode='w', encoding='utf8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(
                    ['token', 'course', 'used', 'used_date', 'used_by',])
        with open('codes.csv', mode='a', encoding='utf8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [generate_token(), course, False, None, None,]
            )

client.run(DISCORD_TOKEN)

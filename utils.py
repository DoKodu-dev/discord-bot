import csv
import logging
from string import ascii_letters, digits
from random import randint

CHARS = ascii_letters + digits + '#$%&@'

def generate_token(lenght: int = 12) -> str:
    token = ''
    for i in range(lenght):
        token += CHARS[randint(0, len(CHARS)-1)]
    return token

def get_role_by_token_from_csv(token: str, csv_token_file: str) -> str:
    try:
        with open(csv_token_file, encoding='utf8') as token_file:
            tokens = list(csv.DictReader(token_file))
    except FileNotFoundError as err:
        logging.error(err)
        return None

    tokens_list = [line['token'] for line in tokens]
    
    try:
        line = tokens[tokens_list.index(token)]
        return line['course']
    except ValueError as err:
        logging.error(err)
        return None
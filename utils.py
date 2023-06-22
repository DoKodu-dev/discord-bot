from string import ascii_letters, digits
from random import randint

CHARS = ascii_letters + digits + '#$%&@'

def generate_token(lenght: int = 12) -> str:
    token = ''
    for i in range(lenght):
        token += CHARS[randint(0, len(CHARS)-1)]
    return token
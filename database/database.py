''' Context manager to manage db '''
from datetime import datetime
import logging
import os
import sqlite3

# pylint: disable=logging-fstring-interpolation
# pylint: disable=unspecified-encoding
# pylint: disable=inconsistent-return-statements


class Database:
    ''' Class to manage db as context manager '''

    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = './database.db'

        if not os.path.exists(db_path):
            with open('./database.db', mode='w'):
                logging.info('Create new database')

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.sql_scripts = './database/sql'

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            logging.error(exc_val)

    def prepare_db(self) -> None:
        ''' Function to prepare db described in 01_initial.sql file,
        operational errors are logging '''
        with open('./database/sql/01_initial.sql') as script_file:
            script = script_file.read()

        try:
            self.cursor.execute(script)
            logging.info('Created table \'tokens\'')
        except sqlite3.OperationalError as err:
            logging.error(f'01_initial.sql: {err}')

    def save_token(self, token: str, course: str) -> None:
        ''' Function to save tokens into db - base on 02_add_token.sql script,
        operational and integrity errors are logging

        Arguments:
            token -- string which will be add to db
            course -- course to which the given token is assigned '''
        with open('./database/sql/02_add_token.sql') as script_file:
            script = script_file.read()

        try:
            self.cursor.execute(script, (token, course))
            self.connection.commit()
        except sqlite3.OperationalError as err:
            logging.error(f'02_add_token.sql: {err}')
            return 'Error'
        except sqlite3.IntegrityError:
            logging.error(f'Token {token} already exist in DB')
            return 'Error'

    def use_token(self, token: str, user: str) -> tuple:
        ''' Function to marking token as used,
        operational errors are logging

        Arguments:
            token -- string which will be check into db and mark as used
            user -- member who used the token

        Returns:
            tuple (row from db) if all went well
                or None if token don't exist, has used before
                or except operational error
        '''
        data = self.get_token(token)
        if data is None:
            logging.warning(f'Token {token} not exist in DB | user: {user}')
            return None
        if data[3] == 0:
            with open('./database/sql/04_mark_token_as_used.sql') as script_file:
                script = script_file.read()

            date = datetime.now()

            try:
                self.cursor.execute(script, (user, date, token))
                self.connection.commit()
                return self.get_token(token)
            except sqlite3.OperationalError as err:
                logging.error(f'04_mark_token_as_used.sql: {err}')
                return None

        logging.error(
            f'Token {token} is used by {data[4]} (date: {data[5]}) | now try to use by {user}')

    def get_token(self, token: str) -> tuple:
        ''' Function to getting row from db searched by token

        Arguments:
            token -- string which will be check into db and mark as used

        Returns:
            tuple (row from db) if all went well
                or None if token don't exist or except operational error
        '''
        with open('./database/sql/03_check_token.sql') as script_file:
            script = script_file.read()

        try:
            self.cursor.execute(script, (token,))
            return self.cursor.fetchone()
        except sqlite3.OperationalError as err:
            logging.error(f'03_check_token.sql: {err}')
    
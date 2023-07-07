import logging
import os
import sqlite3

class Database:
    def __init__(self, db_path: str = None) -> None:
        if db_path is None:
            db_path = './database.db'
            
        if not os.path.exists(db_path):
            with open('./database.db', mode='w'):
                logging.info('Create new database')

        self.connection = sqlite3.connect(db_path) 
        self.cursor = self.connection.cursor()
        self.sql_scripts = './database/sql'

    def prepare_db(self) -> None:
        with open('./database/sql/01_initial.sql') as script_file:
            script = script_file.read()
        
        try:
            self.cursor.execute(script)
            logging.info(f'Created table \'tokens\'')
        except sqlite3.OperationalError as err:
            logging.error(f'01_initial.sql: {err}')

    def save_token(self, token: str, course: str) -> None:
        with open('./database/sql/02_add_token.sql') as script_file:
            script = script_file.read()
        print(script)
        try:
           self.cursor.execute(script, (token, course))
           self.connection.commit()
        except sqlite3.OperationalError as err:
            logging.error(f'02_add_token.sql: {err}')
            return False
        except sqlite3.IntegrityError as err:
            logging.error(f'Token {token} already exist in DB')
            return False
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

    def prepare_db(self):
        list_of_files = list(os.walk(self.sql_scripts))[0]
      
        for i in sorted(list_of_files[2]):
            with open(f'{list_of_files[0]}/{i}') as file:
                scripts = ' '.join(file.readlines()).replace('\n', '').split(';')
                for i, script in enumerate(scripts, start=1):
                    try:
                        self.cursor.execute(script)
                    except sqlite3.OperationalError as err:
                        logging.error(f'{err} -> script {i} in {list_of_files[0]}/{i}')
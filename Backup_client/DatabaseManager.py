from os import path

import mysql.connector

import backup_client
import util


class DatabaseManager:

    def __init__(self):
        self.login = util.load_cred(path.join(backup_client.CREDENTIAL_FILES, "db_login.txt"))
        self.password = util.load_cred(path.join(backup_client.CREDENTIAL_FILES, "db_password.txt"))
        self.connect()

    def connect(self):
        self.db = mysql.connector.connect(
            host="localhost",
            user=self.login,
            passwd=self.password,
            database="backup_client"
        )
        self.cursor = self.db.cursor()

    def insert(self, name, f_hash, key, iv, flags):
        query = ''
        res = self.get(name)

        if not res:
            template = "INSERT INTO files (name,  hash, s_key, iv) VALUES ('{}', '{}', '{}', '{}')"
            query = template.format(name, f_hash, key, iv)
        else:
            if not flags.force:
                util.ColorPrinter.print_warning("File " + name + " is already in your vault.")
                choice = input("Do you want to overwrite it? Y/N: ")
                if choice.lower() not in ["y", 'yeas', "yeah"]:
                    print("Terminating...")
                    exit(0)
            template = "UPDATE files set hash='{}', s_key='{}', iv='{}' WHERE name='{}'"
            query = template.format(f_hash, key, iv, name)

        if flags.verbose: print("Saving crypto parameters...", end='')
        self.cursor.execute(query)
        self.db.commit()
        if flags.verbose: print("OK")

    def get(self, f_name):
        template = "SELECT * FROM files WHERE name='{}'"
        query = template.format(f_name)
        self.cursor.execute(query)
        res = self.cursor.fetchall()
        if res:
            return res[0]
        return res

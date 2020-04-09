#!/usr/bin/python3

import os

import DatabaseManager
import FileCipher
import FileManager
import client_auth
import util

CREDENTIAL_FILES = "LOGIN_CREDENTIALS"
ENCRYPTION_POOL = "encryption_pool"
DOWNLOAD_FOLDER = "/home/kiko/Desktop/drive_downloaded"
DB_ENTRY_KEY_OFFSET = 3
DB_ENTRY_IV_OFFSET = 4


class Client:

    def __init__(self):
        self.listed_files = []
        print("Connecting to the database...      ", end="")
        self.printer = util.ColorPrinter()

        self.db_m = DatabaseManager.DatabaseManager()
        print(" OK")

        print("Authorizing against google drive... ", end="")
        self.service = client_auth.authorize()

        print("OK")
        self.man = FileManager.FileManager()

        self.cip = FileCipher.FileCipher()

        msg = "\n---------------------------------\n" \
              "| Welcome to the Backup Client! |\n" \
              "---------------------------------\n"
        self.printer.print_green(msg)

    def upload_file(self, f_path):
        iv = self.cip.generate_bytes(16)
        key = self.cip.generate_bytes(32)
        f_bytes = util.get_file_bytes(f_path)
        f_hash = self.cip.compute_hash(f_bytes)
        self.db_m.insert(util.get_file_name(f_path), f_path, f_hash, key.hex(), iv.hex())

        enc_file_name = self.cip.encrypt_file(f_path, key, iv)

        self.man.upload(enc_file_name, self.service)

        os.remove(enc_file_name)

    def update_listed_files(self):
        self.listed_files = self.man.list_files(self.service)

    def download_file(self, id, path, name):
        self.man.download(self.service, id, path, name)

    def decrypt_file(self, f_path, name, res_path):
        decr_name = util.remove_cipher_extension(name)
        entry = self.db_m.get(decr_name)
        passw = bytes(bytearray.fromhex(entry[DB_ENTRY_KEY_OFFSET]))
        iv = bytes(bytearray.fromhex(entry[DB_ENTRY_IV_OFFSET]))

        self.cip.decrypt_file(os.path.join(f_path, name), passw, iv, res_path, decr_name)


def main():
    b_cl = Client()

    b_cl.upload_file("/home/kiko/Desktop/Backup-Client/picture.gif")

    b_cl.update_listed_files()

    choice = input("Select: ")
    choice = int(choice)
    res = list(filter(lambda x: x["id"] == b_cl.listed_files[choice - 1]["id"], b_cl.listed_files))[0]

    b_cl.download_file(res["id"], ENCRYPTION_POOL, res["name"])

    b_cl.decrypt_file(ENCRYPTION_POOL, res["name"], DOWNLOAD_FOLDER)

    os.remove(os.path.join(ENCRYPTION_POOL, res["name"]))

    # man.create_folder(service, "tmp")

    # man.search_file(service, "LICENSE")


if __name__ == '__main__':
    main()

    """
    https://developers.google.com/drive/api/v3/search-files
    
    """

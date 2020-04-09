#!/usr/bin/python3

import argparse
import os

import DatabaseManager
import FileCipher
import FileManager
import client_auth
import util

CREDENTIAL_FILES = "/home/kiko/.LOGIN_CREDENTIALS"
ENCRYPTION_POOL = "/tmp/encryption_pool"
DOWNLOAD_FOLDER = "/home/kiko/Desktop/drive_downloaded"
DB_ENTRY_HASH_OFFSET = 1
DB_ENTRY_KEY_OFFSET = 2
DB_ENTRY_IV_OFFSET = 3


class Client:

    def __init__(self, flags):
        self.flags = flags
        self.listed_files = []
        self.ls_chached = False

        if self.flags.verbose: print("Connecting to the database...      ", end="")

        self.db_m = DatabaseManager.DatabaseManager()

        if self.flags.verbose: print(" OK")

        if self.flags.verbose: print("Authorizing against google drive... ", end="")

        self.service = client_auth.authorize()

        if self.flags.verbose: print("OK")

        self.man = FileManager.FileManager()

        self.cip = FileCipher.FileCipher()

    def upload_file(self, f_path):

        if not os.path.exists(f_path):
            util.ColorPrinter.print_fail("Pleas double check your file name.")
            exit(1)
        iv = self.cip.generate_bytes(16)
        key = self.cip.generate_bytes(32)
        f_bytes = util.get_file_bytes(f_path)
        f_hash = self.cip.compute_hash(f_bytes)

        self.db_m.insert(util.get_file_name(f_path), f_hash, key.hex(), iv.hex(), self.flags)

        if self.flags.verbose: print("Encrypting...", end='')
        enc_file_name = self.cip.encrypt_file(f_path, key, iv, self.flags)

        if self.flags.verbose: print("OK")

        if self.flags.verbose: print("Uploading ...", end='')

        self.man.upload(enc_file_name, self.service)
        self.ls_chached = False

        if self.flags.verbose: print("OK")

        if self.flags.verbose: print("Deleting tmp files... ", end='')
        os.remove(enc_file_name)
        if self.flags.verbose: print("OK")

        util.ColorPrinter.print_green("Uploaded.")

    def update_listed_files(self):
        self.listed_files = self.man.list_files(self.service)
        self.ls_chached = True

    def download_file(self, id, path, name):
        self.man.download(self.service, id, path, name)

    def decrypt_file(self, f_path, name, res_path):
        decr_name = util.remove_cipher_extension(name)
        entry = self.db_m.get(decr_name)
        passw = bytes(bytearray.fromhex(entry[DB_ENTRY_KEY_OFFSET]))
        iv = bytes(bytearray.fromhex(entry[DB_ENTRY_IV_OFFSET]))

        self.cip.decrypt_file(os.path.join(f_path, name), passw, iv, res_path, decr_name)

    def select_and_download_file(self):
        self.update_listed_files()

        choice = input("Select: ")
        choice = int(choice)
        res = list(filter(lambda x: x["id"] == self.listed_files[choice - 1]["id"], self.listed_files))[0]

        self.download_file(res["id"], ENCRYPTION_POOL, res["name"])

        self.decrypt_file(ENCRYPTION_POOL, res["name"], DOWNLOAD_FOLDER)

        os.remove(os.path.join(ENCRYPTION_POOL, res["name"]))

    def select_file_blind(self, file_name):
        res = self.man.search_file(self.service, file_name)

        if len(res) > 1:
            util.prettify_listing(res)

            choice = -1
            while choice < 1 or choice >= len(res):
                choice = input("Which one did you mean?: [index] or x to exit:")
                util.terminate(choice)
                choice = int(choice)
            return res[choice - 1]

        if len(res) == 1:
            return res[0]

        print("File " + file_name + " isn't present in your vault.")
        if not (self.ls_chached):
            self.update_listed_files()
        util.prettify_listing(self.listed_files)

        choice = -1
        while choice < 1 or choice >= len(self.listed_files):
            choice = input("Choose file to download by entering it's number or enter 'x' to exit: ")
            util.terminate(choice)
            choice = int(choice)
        return self.listed_files[choice - 1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="enable verbose mode")
    parser.add_argument("-f", "--force", action='store_true', help="overwrite files without asking")
    parser.add_argument("action", type=str, help="UPLOAD / DOWNLOAD / DIFF")
    parser.add_argument("action_arg", nargs='?', help="[file name]")

    return parser.parse_args()


def main():
    if not os.path.exists(ENCRYPTION_POOL):
        os.mkdir(ENCRYPTION_POOL)

    b_cl = Client(parse_args())

    if b_cl.flags.action.lower() in ["u", "up", "upload"]:
        abs_path = os.path.abspath(b_cl.flags.action_arg)
        b_cl.upload_file(abs_path)

    elif b_cl.flags.action.lower() in ["l", "ls", "list"]:
        if not b_cl.ls_chached:
            b_cl.update_listed_files()
        util.prettify_listing(b_cl.listed_files)


    elif b_cl.flags.action.lower() in ["download", "d", "down"]:
        f_file = b_cl.select_file_blind(b_cl.flags.action_arg)
        print("Downloading" + f_file["name"] + "...")
        b_cl.download_file(f_file["id"], DOWNLOAD_FOLDER, f_file["name"])

    elif b_cl.flags.action.lower() in ["diff"]:
        file_bytes = util.get_file_bytes(b_cl.flags.action_arg)  # TODO: check path, if incorrect -> list files
        hash = b_cl.cip.compute_hash(file_bytes)
        f_name = util.get_file_name(b_cl.flags.action_arg)
        query_res = b_cl.db_m.get(f_name)
        if not query_res:
            print(f_name + "is not in your vault.")
        cloud_hash = query_res[0][DB_ENTRY_HASH_OFFSET]
        if hash == cloud_hash:
            print("Files are identical.")
        else:
            print("Files are different")
    else:
        print("Incorrect argument " + b_cl.flags.action_arg + ".\nUse -h for help.")


if __name__ == '__main__':
    main()

    """
    https://developers.google.com/drive/api/v3/search-files
    
    """

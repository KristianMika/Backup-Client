#!/usr/bin/python3

import argparse
import os

import FileCipher
import FileManager
import client_auth
import util

CREDENTIAL_FILES = "/home/kiko/.LOGIN_CREDENTIALS"
ENCRYPTION_POOL = "/tmp/encryption_pool"
DOWNLOAD_FOLDER = ""
DB_ENTRY_HASH_OFFSET = 1
DB_ENTRY_KEY_OFFSET = 2
DB_ENTRY_IV_OFFSET = 3
AES_KEY_SIZE = 32


class Client:

    def __init__(self, flags):
        self.flags = flags
        self.listed_files = []
        self.ls_chached = False

        if self.flags.verbose: print("Authorizing against google drive... ", end="")

        self.service = client_auth.authorize()

        if self.flags.verbose: print("OK")

        self.man = FileManager.FileManager()

        self.cip = FileCipher.FileCipher()

        self.key = util.get_file_bytes(os.path.join(CREDENTIAL_FILES, "key.secret"))

        self.name_iv = util.get_file_bytes(os.path.join(CREDENTIAL_FILES, "iv.secret"))

    def upload_file(self, f_path):

        if not os.path.exists(f_path):
            util.ColorPrinter.print_fail("Pleas double check your file name.")
            exit(1)
        iv = self.cip.generate_bytes(16)

        f_bytes = util.get_file_bytes(f_path)

        if self.flags.verbose: print("Encrypting...", end='')
        enc_file_name = self.cip.encrypt_file(f_path, self.key, iv, self.name_iv)

        if self.flags.verbose: print("OK")

        if self.flags.verbose: print("Uploading ...", end='')

        self.man.upload(enc_file_name, self.service)
        self.ls_chached = False

        if self.flags.verbose: print("OK")

        if self.flags.verbose: print("Deleting tmp files... ", end='')
        os.remove(enc_file_name)
        if self.flags.verbose: print("OK")

        util.ColorPrinter.print_green("Uploaded.")

    def download_file(self, id, path, name):
        self.man.download(self.service, id, path, name)

    def decrypt_file(self, f_path, name, res_path):
        decr_name = util.remove_cipher_extension(name)

        self.cip.decrypt_file(os.path.join(f_path, name), self.key, res_path, self.name_iv)

    def select_and_download_file(self):
        files = self.man.list_files(self.service)
        choice = input("Select: ")
        choice = int(choice)
        res = list(filter(lambda x: x["id"] == files[choice - 1]["id"], files))[0]

        self.download_file(res["id"], ENCRYPTION_POOL, res["name"])

        self.decrypt_file(ENCRYPTION_POOL, res["name"], DOWNLOAD_FOLDER)

        os.remove(os.path.join(ENCRYPTION_POOL, res["name"]))

    def gen_key_file(self):
        key = self.cip.generate_bytes(AES_KEY_SIZE)
        util.write_file_bytes(key, CREDENTIAL_FILES, "key.secret")

    def gen_iv_file(self):
        key = self.cip.generate_bytes(16)
        util.write_file_bytes(key, CREDENTIAL_FILES, "iv.secret")

    def list_files(self, files=None):
        if not files:
            files = self.man.list_files(self.service)
        dec_names = []
        for file in files:
            dec_names.append(self.cip.decrypt_filename(file["name"], self.key, self.name_iv))
        util.prettify_listing(dec_names)
        return files

    def select_file_blind(self, file_name):
        enc_name = self.cip.encrypt_filename(file_name, self.key, self.name_iv)
        res = self.man.search_file(self.service, enc_name)

        if len(res) > 1:
            self.list_files(res)

            choice = -1
            while choice < 1 or choice > len(res):
                choice = input("Which one did you mean?: [index] or x to exit:")
                util.terminate(choice)
                choice = int(choice)
            return res[choice - 1]

        if len(res) == 1:
            return res[0]

        util.ColorPrinter.print_fail('Error ocured while locating your file.')

        files = self.list_files()

        if not files:
            exit(0)
        choice = -1
        while choice < 1 or choice > len(files):
            choice = input("Choose file to download by entering it's number or enter 'x' to exit: ")
            util.terminate(choice)
            choice = int(choice)
        return files[choice - 1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="enable verbose mode")
    parser.add_argument("-f", "--force", action='store_true', help="overwrite files without asking")
    parser.add_argument("action", type=str, help="UPLOAD / DOWNLOAD")
    parser.add_argument("action_arg", nargs='?', help="[file name]")

    return parser.parse_args()


def main():
    DOWNLOAD_FOLDER = os.getcwd()
    if not os.path.exists(ENCRYPTION_POOL):
        os.mkdir(ENCRYPTION_POOL)

    b_cl = Client(parse_args())

    if b_cl.flags.action.lower() in ["u", "up", "upload"]:
        abs_path = os.path.abspath(b_cl.flags.action_arg)
        b_cl.upload_file(abs_path)

    elif b_cl.flags.action.lower() in ["l", "ls", "list"]:
        b_cl.list_files()


    elif b_cl.flags.action.lower() in ["download", "d", "down"]:
        f_file = b_cl.select_file_blind(b_cl.flags.action_arg)
        b_cl.download_file(f_file["id"], ENCRYPTION_POOL, f_file["name"])
        print("Decrypting ...")
        b_cl.decrypt_file(ENCRYPTION_POOL, f_file["name"], DOWNLOAD_FOLDER)
        util.ColorPrinter.print_green("Done")

    elif b_cl.flags.action.lower() in ["del", "delete", "remove", "rm"]:
        f_file = b_cl.select_file_blind(b_cl.flags.action_arg)
        choice = input("Are you sure? [Y/N]: ")
        if choice.lower() not in ["y", "yes", "yeah"]:
            print("Terminating... ")
            exit(0)

        print("Deleting ...")
        b_cl.man.delete(b_cl.service, f_file)
        util.ColorPrinter.print_green("Deleted")

    else:
        print("Incorrect argument " + b_cl.flags.action + ".\nUse -h for help.")


if __name__ == '__main__':
    main()

    """
    https://developers.google.com/drive/api/v3/search-files
    
    """

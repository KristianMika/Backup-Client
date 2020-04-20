#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
import os

import httplib2

import FileCipher
import FileManager
import client_auth
import util

CREDENTIAL_FILES = "~/.VAULT_CREDENTIALS"
ENCRYPTION_POOL = "/tmp/encryption_pool"

AES_KEY_SIZE = 32
IV_SIZE = 16


class Client:
    """ The top class that executes user's requests """

    def __init__(self, flags, cred_dir):

        self.flags = flags

        self.CREDENTIAL_FILES = os.path.expanduser(cred_dir)

        self.cipher = FileCipher.FileCipher()

        self.key = self.load_key(os.path.join(self.CREDENTIAL_FILES, "key.secret"))

        self.download_folder = os.getcwd()

        if self.flags.verbose: print("Authenticating against google drive... ", end="")

        try:
            self.service = client_auth.authenticate(self.CREDENTIAL_FILES)

        except httplib2.ServerNotFoundError:

            util.ColorPrinter.print_fail("Authentication failed! Please, check your Internet connection. ")
            exit(1)

        if self.flags.verbose: print("OK")

        self.manager = FileManager.FileManager(self.service)

    def load_key(self, f_path):
        """ Loads key used for encryption """

        key = ''
        if not os.path.exists(f_path):
            key = self.cipher.generate_bytes(AES_KEY_SIZE)

            print("Couldn't find \"key.secret\" \nGenerating a new one")
            if not util.read_y_n("Continue? [Y/N]: "):
                print("Terminating...")
                exit(1)

            util.write_file_bytes(key, self.CREDENTIAL_FILES, "key.secret", False)
        else:
            return util.get_file_bytes(f_path)

        return key

    def upload_file(self, f_path):
        """ Encrypts and uploads file at <f_path>"""

        if not os.path.exists(f_path):
            util.ColorPrinter.print_fail("Please double-check your file name.")
            exit(1)

        iv = self.cipher.generate_bytes(IV_SIZE)

        if self.flags.verbose: print("Encrypting...", end='')

        enc_file_name = self.cipher.encrypt_file(f_path, self.key, iv, self.flags.force, ENCRYPTION_POOL)

        if self.flags.verbose: print("OK\nUploading ...")

        self.manager.upload(enc_file_name)

        if self.flags.verbose: print("OK\nDeleting tmp files... ", end='')

        os.remove(enc_file_name)

        if self.flags.verbose: print("OK")

        util.ColorPrinter.print_green("Done.")

    def list_files(self, files=None):
        """ Download file names from the drive, decrypts them and prints them.
            It can also take a list of files as an argument."""

        if not files:
            files = self.manager.list_files()

        dec_names = []
        for file in files:
            dec_names.append(self.cipher.decrypt_filename(file["name"], self.key))

        util.prettify_listing(dec_names)

        return files

    def select_file_blindly(self, file_name):
        """ Firstly, it encrypts the <file_name> entered by the user and searches for it in the drive.
            If the file_name isn't precise, it lists all the files and lets the user choose one """

        res = []
        # encrypt filename and search for it in the drive
        if file_name:
            enc_name = self.cipher.encrypt_filename(file_name, self.key)
            res = self.manager.search_file(enc_name)

        if len(res) == 1:
            return res[0]

        files = self.list_files()

        if not files:
            exit(0)

        choice = ''
        while not choice.isdigit() or int(choice) < 1 or int(choice) > len(files):
            choice = input("Choose a file to download by entering it's number or enter 'x' to exit: ")
            util.terminate(choice)

        return files[int(choice) - 1]

    def download_file(self, file_id, f_enc_name, o_path=None):
        """ Downloads file with the correct <file_id>, decrypts it,
         decrypts it's filename and stores it to <o_path> """

        if not o_path:
            o_path = self.download_folder
        else:
            o_path = os.path.abspath(o_path)

            if not os.path.exists(o_path):
                util.ColorPrinter.print_fail("Folder " + o_path + " does not exist.")
                exit(0)

        self.manager.download(file_id, ENCRYPTION_POOL, f_enc_name)

        if self.flags.verbose: print("Decrypting ...")

        self.cipher.decrypt_file(os.path.join(ENCRYPTION_POOL, f_enc_name), self.key, o_path, self.flags.force)

        os.remove(os.path.join(ENCRYPTION_POOL, f_enc_name))

        if self.flags.verbose: util.ColorPrinter.print_green("Done")


def parse_args():
    """ Parses CL arguments """

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action='store_true', help="enable verbose mode")
    parser.add_argument("-f", "--force", action='store_true', help="overwrite files without asking")
    parser.add_argument('-o', "--output", type=str, help="selects output path")
    parser.add_argument("action", type=str, help="UPLOAD / DOWNLOAD / LIST")
    parser.add_argument("action_arg", nargs='?', help="[file name]")

    return parser.parse_args()


def main():
    """ The main method only calls methods according to the parsed CL arguments  """

    if not os.path.exists(ENCRYPTION_POOL):
        os.mkdir(ENCRYPTION_POOL)

    b_client = Client(parse_args(), CREDENTIAL_FILES)

    # Uploads the file
    if b_client.flags.action.lower() in ["u", "up", "upload"]:
        abs_path = os.path.abspath(b_client.flags.action_arg)
        b_client.upload_file(abs_path)

    # Lists the drive
    elif b_client.flags.action.lower() in ["l", "ls", "list"]:
        b_client.list_files()

    # Downloads the file
    elif b_client.flags.action.lower() in ["download", "d", "down"]:
        f_file = b_client.select_file_blindly(b_client.flags.action_arg)
        b_client.download_file(f_file["id"], f_file["name"], b_client.flags.output)

    # Removes the file
    elif b_client.flags.action.lower() in ["del", "delete", "remove", "rm"]:
        f_file = b_client.select_file_blindly(b_client.flags.action_arg)

        if not util.read_y_n("Are you sure? [Y/N]: "):
            exit(0)

        if b_client.flags.verbose: print("Deleting ...")
        b_client.manager.delete(f_file)
        if b_client.flags.verbose: util.ColorPrinter.print_green("Done")

    # In case the action argument is incorrect
    else:
        print("Incorrect argument \"" + b_client.flags.action + "\".\nUse -h for help.")
        exit(1)


if __name__ == '__main__':
    main()

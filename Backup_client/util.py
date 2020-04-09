import io
import os


def load_cred(path):
    with open(path, "r") as file:
        return file.readline()


def save_file(fh, path, name):
    with io.open(os.path.join(path, name), "wb") as file:
        fh.seek(0)
        file.write(fh.read())


def prettify_listing(items):
    if len(items) > 1:
        print("{} items".format(len(items)))
    elif len(items) == 1:
        print("{} item".format(len(items)))
    else:
        print("Your vault is empty")
        return
    i = 1
    for item in items:
        print("{}. {} ({})".format(i, item["name"], item["mimeType"]))
        i += 1
    print()


def get_file_bytes(path):
    with open(path, "rb") as file:
        bytes = file.read()
    return bytes


def write_file_bytes(bytes, f_path, f_name):
    with open(os.path.join(f_path, f_name), "wb") as file:
        file.write(bytes)


def get_file_name(path):
    return path.split("/")[-1]


def remove_cipher_extension(file):
    if len(file) > 7 and file[-7:] == ".cipher":
        return file[:-7]
    return file


def pad(bytes, mod_len):
    return bytes + (b'0' * (mod_len - len(bytes) % mod_len))


def print_if_verbose(flags, msg, clr):
    if flags.verbose:
        print(clr + msg + clr)


def unpad(bytes):
    last_ind = len(bytes) - 1

    while last_ind >= 0:
        if bytes[last_ind] == ord(b'0'):
            last_ind -= 1
        else:
            break
    return bytes[:last_ind + 1]


def terminate(choice):
    if choice in ["x", "X", "exit", "EXIT"]:
        print("Terminating...")
        exit(0)


class ColorPrinter:

    @staticmethod
    def print_green(msg):
        print('\033[92m' + msg + '\033[0m')

    @staticmethod
    def print_blue(msg):
        print('\033[94m' + msg + '\033[0m')

    @staticmethod
    def print_warning(msg):
        print('\033[93m' + msg + '\033[0m')

    @staticmethod
    def print_fail(msg):
        print('\033[91m' + msg + '\033[0m')

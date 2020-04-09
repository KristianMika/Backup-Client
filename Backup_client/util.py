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
    print("<ls>: ({}) items".format(len(items)))
    i = 1
    for item in items:
        print("{}. {} ({})".format(i, item["name"], item["mimeType"]))
        i += 1
    print()


def get_file_bytes(path):
    bytes = []
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


def unpad(bytes):
    last_ind = len(bytes) - 1

    while last_ind >= 0:
        if bytes[last_ind] == ord(b'0'):
            last_ind -= 1
        else:
            break
    return bytes[:last_ind + 1]


class ColorPrinter:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def print_green(self, msg):
        print(self.GREEN + msg + self.ENDC)

    def print_blue(self, msg):
        print(self.BLUE + msg + self.ENDC)

    def print_warning(self, msg):
        print(self.WARNING + msg + self.ENDC)

    def print_fail(self, msg):
        print(self.FAIL + msg + self.ENDC)


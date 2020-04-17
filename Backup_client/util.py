import io
import os


def save_file(fh, path, name):
    """ Saves BytesIO stream into path/name """

    with io.open(os.path.join(path, name), "wb") as file:
        fh.seek(0)
        file.write(fh.read())


def prettify_listing(items):
    """ Prints file names, one filename per line """

    if len(items) > 1:
        print("{} item".format(len(items)))

    elif len(items) == 1:
        print("{} item".format(len(items)))

    else:
        print("Your vault is empty")
        return

    for index, f_name in enumerate(items, start=1):
        print("{}. {}".format(index, f_name))


def get_file_bytes(path):

    """ Reads file content (binary)  """

    with open(path, "rb") as file:
        f_bytes = file.read()

    return f_bytes


def write_file_bytes(bytes, f_path, f_name, forced):
    f_path = os.path.join(f_path, f_name)
    if os.path.exists(f_path) and not forced:
        ColorPrinter.print_warning("File \"" + f_name + "\" already exists.")
        choice = input("Do you want to overwrite it? [Y/N]: ")
        if not read_y_n(choice):
            print("Terminating...")
            exit(0)

    with open(f_path, "wb") as file:
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


def read_y_n(inp):
    if inp.lower() in ['y', 'yep', 'yeah', 'yes']:
        return True
    return False


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

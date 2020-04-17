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


def write_file_bytes(f_bytes, f_path, f_name, forced):
    """ Writes byte content into a file
        If the file already exists, prompts the user if it should be overwritten"""

    f_path = os.path.join(f_path, f_name)

    if os.path.exists(f_path) and not forced:
        ColorPrinter.print_warning("File \"" + f_name + "\" already exists.")
        choice = input("Do you want to overwrite it? [Y/N]: ")

        if not read_y_n(choice):
            print("Terminating...")
            exit(0)

    with open(f_path, "wb") as file:
        file.write(f_bytes)


def get_file_name(path):
    """ Takes a path and returns only the filename """

    return os.path.split(path)[-1]


def remove_cipher_extension(file):
    """ Removes the '.cipher' extension if present """

    if len(file) > 7 and file[-7:] == ".cipher":
        return file[:-7]

    return file


def pad(f_bytes, mod_len):
    """ Pads the file bytes to the nearest multiple of mod_len  """

    return f_bytes + (b'0' * (mod_len - len(f_bytes) % mod_len))


def unpad(f_bytes):
    """ Removes padding from the file bytes """

    last_i = len(f_bytes) - 1

    while last_i >= 0:
        if f_bytes[last_i] == ord(b'0'):
            last_i -= 1
        else:
            break

    return f_bytes[:last_i + 1]


def terminate(choice):
    """ Takes user's input as an argument and terminates the program according to choice """

    if choice.lower() in ["x", "exit", ]:
        print("Terminating...")
        exit(0)


def read_y_n(inp):
    """ Takes user's input as an argument and translates it to bool """

    if inp.lower() in ['y', 'yep', 'yeah', 'yes']:
        return True
    return False


class ColorPrinter:
    """ Class that prints colorful text """

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

import io
import os


def save_file(fh):
    curr_dir = os.getcwd()
    with io.open(os.path.join(curr_dir, "new_file.jpg"), "wb") as file:
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


def write_file_bytes(bytes, path):
    # with open(path, "wb") as file:
    with open(path + ".cipher", "wb") as file:
        file.write(bytes)

    return path + ".cipher"


def get_file_name(path):
    return path.split("/")[-1]


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

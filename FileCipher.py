from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import util


class FileCipher:

    def encrypt_file(self, path, key, iv):
        obj = AES.new(key, AES.MODE_CBC, iv)
        file = util.get_file_bytes(path)
        file = util.pad(file, AES.block_size)
        cipher = obj.encrypt(file)
        return util.write_file_bytes(cipher, path)

    def generate_bytes(self, n):
        return get_random_bytes(n)

    def decrypt_file(self, path, key, iv, res_path):
        obj2 = AES.new(key, AES.MODE_CBC, iv)
        cipher = util.get_file_bytes(path)
        plain = bytes(obj2.decrypt(cipher))
        plain = util.unpad(plain)
        util.write_file_bytes(plain, res_path)

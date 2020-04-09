from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

import backup_client
import os
import util


class FileCipher:

    def encrypt_file(self, path, key, iv, flags):
        f_bytes = util.get_file_bytes(path)
        cipher = self.encrypt_bytes(f_bytes, key, iv)
        f_name = util.get_file_name(path) + ".cipher"
        util.write_file_bytes(cipher, backup_client.ENCRYPTION_POOL, f_name)
        return os.path.join(backup_client.ENCRYPTION_POOL, f_name)

    def encrypt_bytes(self, f_bytes, key, iv):
        obj = AES.new(key, AES.MODE_CBC, iv)
        f_bytes = util.pad(f_bytes, AES.block_size)
        cipher = obj.encrypt(f_bytes)
        return cipher

    def generate_bytes(self, n):
        return get_random_bytes(n)

    def decrypt_file(self, path, key, iv, res_path, res_name):
        obj2 = AES.new(key, AES.MODE_CBC, iv)
        cipher = util.get_file_bytes(path)
        plain = bytes(obj2.decrypt(cipher))
        plain = util.unpad(plain)
        util.write_file_bytes(plain, res_path, res_name)

    def compute_hash(self, file):
        sha_obj = SHA256.new()
        sha_obj.update(file)
        dig = sha_obj.hexdigest()
        return dig

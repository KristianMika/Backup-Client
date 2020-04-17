import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import backup_client
import util


class FileCipher:

    def encrypt_file(self, path, key, iv, name_iv, f):
        f_bytes = util.get_file_bytes(path)
        cipher = self.encrypt_bytes(f_bytes, key, iv)

        enc_name = self.encrypt_filename(util.get_file_name(path), key, name_iv)

        f_name = enc_name + ".cipher"
        util.write_file_bytes(iv + cipher, backup_client.ENCRYPTION_POOL, f_name, f)
        return os.path.join(backup_client.ENCRYPTION_POOL, f_name)

    def encrypt_bytes(self, f_bytes, key, iv):
        obj = AES.new(key, AES.MODE_CBC, iv)
        f_bytes = util.pad(f_bytes, AES.block_size)
        cipher = obj.encrypt(f_bytes)
        return cipher

    def encrypt_filename(self, name, key, name_iv):
        obj = AES.new(key, AES.MODE_CBC, name_iv)
        name = util.pad(name.encode(), AES.block_size)
        cipher = obj.encrypt(name)
        return cipher.hex()

    def decrypt_filename(self, cipher, key, name_iv):
        obj = AES.new(key, AES.MODE_CBC, name_iv)
        name = obj.decrypt(bytes.fromhex(util.remove_cipher_extension(cipher)))
        return util.unpad(name).decode()

    def generate_bytes(self, n):
        return get_random_bytes(n)

    def decrypt_file(self, path, key, res_path, name_iv, f):
        cipher = util.get_file_bytes(path)
        iv = cipher[:16]
        cipher = cipher[16:]
        obj2 = AES.new(key, AES.MODE_CBC, iv)
        plain = bytes(obj2.decrypt(cipher))
        plain = util.unpad(plain)

        res_name = self.decrypt_filename(util.remove_cipher_extension(util.get_file_name(path)), key, name_iv)
        util.write_file_bytes(plain, res_path, res_name, f)
        return res_name

import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

import backup_client
import util


class FileCipher:
    """ Class that manages all cryptographic methods """

    def encrypt_bytes(self, f_bytes, key, iv):
        """ Encrypts f_bytes using AES in CBC mode """

        AES_cip = AES.new(key, AES.MODE_CBC, iv)
        f_bytes = util.pad(f_bytes, AES.block_size)
        cipher = AES_cip.encrypt(f_bytes)

        return cipher

    def encrypt_file(self, path, key, iv, name_iv, f):
        """ Encrypts the <path> file located in  and """
        f_bytes = util.get_file_bytes(path)
        cipher = self.encrypt_bytes(f_bytes, key, iv)

        enc_name = self.encrypt_filename(util.get_file_name(path), key)

        f_name = enc_name + ".cipher"
        util.write_file_bytes(iv + cipher, backup_client.ENCRYPTION_POOL, f_name, f)
        return os.path.join(backup_client.ENCRYPTION_POOL, f_name)

    def encrypt_filename(self, name, key):
        """ Encrypts filename using AES in ECB mode """

        AES_cipher = AES.new(key, AES.MODE_ECB)
        name = util.pad(name.encode(), AES.block_size)
        cipher = AES_cipher.encrypt(name)

        return cipher.hex()

    def decrypt_filename(self, cipher, key):
        """ Decrypts filename using AES in ECB mode """

        AES_cipher = AES.new(key, AES.MODE_ECB)
        name = AES_cipher.decrypt(bytes.fromhex(util.remove_cipher_extension(cipher)))

        return util.unpad(name).decode()

    def decrypt_file(self, path, key, res_path, force):
        """ Decrypts the file located in <path> and stores it as res_path/<encrypted file name>
            File names are encrypted using the same <name_iv> stored is the <CREDENTIALS> folder """

        cipher = util.get_file_bytes(path)

        # encrypted file == 16B IV | xB encrypted file content
        iv = cipher[:backup_client.IV_SIZE]
        cipher = cipher[backup_client.IV_SIZE:]

        AES_cip = AES.new(key, AES.MODE_CBC, iv)
        plain = bytes(AES_cip.decrypt(cipher))
        plain = util.unpad(plain)

        res_name = self.decrypt_filename(util.remove_cipher_extension(util.get_file_name(path)), key)
        util.write_file_bytes(plain, res_path, res_name, force)
        return res_name

    def generate_bytes(self, n):
        """ Generates <n> random bytes """

        return get_random_bytes(n)

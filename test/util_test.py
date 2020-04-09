import util
import unittest


class TestUtil(unittest.TestCase):
    def test_get_file_name(self):
        self.assertEqual(util.get_file_name("/home/Desktop/file.txt"), "file.txt")
        self.assertEqual(util.get_file_name("./file.txt"), "file.txt")

    def test_remove_cipher_extension(self):
        self.assertEqual(util.remove_cipher_extension("/home/file.png.cipher"), "/home/file.png")
        self.assertEqual(util.remove_cipher_extension("file.png.cipher"), "file.png")
        self.assertEqual(util.remove_cipher_extension("/home/file.png"), "/home/file.png")
if __name__ == "__main__":
    unittest.main()
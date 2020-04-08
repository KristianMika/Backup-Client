import util
import unittest


class TestUtil(unittest.TestCase):
    def test_get_file_name(self):
        self.assertEqual(util.get_file_name("/home/Desktop/file.txt"), "file.txt")
        self.assertEqual(util.get_file_name("./file.txt"), "file.txt")


if __name__ == "__main__":
    unittest.main()
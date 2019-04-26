import unittest
import help
import os


class Testhelp(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_for_word(self):
        self.assertEqual(help.check_for_word("hallo"), True)
        self.assertEqual(help.check_for_word("help"), True)
        self.assertEqual(help.check_for_word("status"), True)
        self.assertEqual(help.check_for_word("lijst"), True)
        self.assertEqual(help.check_for_word("aan"), True)
        self.assertEqual(help.check_for_word("uit"), True)
        self.assertEqual(help.check_for_word("documentatie"), True)
        self.assertEqual(help.check_for_word("confugureer"), True)
        self.assertEqual(help.check_for_word("conf"), None)

    def test_sleutels_str(self):
        self.assertIsInstance(help.sleutels_str(), str)

    print(os.getenv('GITHUB_TOKEN'))


if __name__ == "__main__":
    unittest.main()


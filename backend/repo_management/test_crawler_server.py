import unittest

from repo_management.crawler_server import extract_repo_name_from_url


class MyTestCase(unittest.TestCase):
    def test_extract_repo_name_from_url(self):
        urls = [
            'git@github.com:TelegramMessenger/Telegram-iOS.git',
            'https://github.com/TelegramMessenger/Telegram-iOS.git'
        ]

        names = [extract_repo_name_from_url(url) for url in urls]

        expected_names = ['Telegram-iOS', 'Telegram-iOS']
        self.assertEqual(names, expected_names)


if __name__ == '__main__':
    unittest.main()

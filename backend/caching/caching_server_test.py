import unittest

from caching.caching_server import Store


class StoreTest(unittest.TestCase):
    def test_set_and_get(self):
        store = Store()

        store.set_value('myCategory', 'a', 123)

        self.assertEqual(store.get_value('myCategory', 'a'), 123)

    def test_with_limit(self):
        store = Store()

        store.set_value('myCategory', 'a', 123, limit=1)
        store.set_value('myCategory', 'b', 234, limit=1)

        self.assertIsNone(store.get_value('myCategory', 'a'))
        self.assertEqual(store.get_value('myCategory', 'b'), 234)

    def test_lru(self):
        store = Store()

        store.set_value('myCategory', 'a', 123, limit=2)
        store.set_value('myCategory', 'b', 234, limit=2)
        store.get_value('myCategory', 'a')
        store.set_value('myCategory', 'c', 345, limit=2)

        self.assertIsNone(store.get_value('myCategory', 'b'))


if __name__ == '__main__':
    unittest.main()

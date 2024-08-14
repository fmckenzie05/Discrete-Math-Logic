import unittest
from tries_1 import PrefixTree

class TrieTest(unittest.TestCase):

    def setUp(self):
        """Initialize a new PrefixTree for each test."""
        self.trie = PrefixTree()

    def test_insert_and_find(self):
        """Test inserting and finding words."""
        self.trie.insert('apple')
        self.assertIsNotNone(self.trie.find('apple'))
        self.assertIsNone(self.trie.find('app'))
        self.trie.insert('app')
        self.assertIsNotNone(self.trie.find('app'))

    def test_starts_with(self):
        """Test finding words with a given prefix."""
        self.trie.insert('apple')
        self.trie.insert('appreciate')
        self.trie.insert('aposematic')
        self.trie.insert('apoplectic')
        self.trie.insert('appendix')
        results = self.trie.starts_with('app')
        self.assertIn('apple', results)
        self.assertIn('appreciate', results)
        self.assertIn('appendix', results)

    def test_trie_size(self):
        """Test the size of the Trie."""
        self.trie.insert('bad')
        self.trie.insert('bat')
        self.trie.insert('cat')
        self.trie.insert('cage')
        self.assertEqual(self.trie.size(), 10)

    def test_visualize(self):
        """Test visualizing the Trie."""
        self.trie.insert('bat')
        self.trie.insert('battle')
        self.trie.insert('battery')
        self.trie.insert('bath')
        self.trie.insert('bathroom')
        # Attempting to visualize the Trie
        try:
            self.trie.visualize('bat')
        except Exception as e:
            self.fail(f"Visualization failed with exception: {e}")

if __name__ == '__main__':
    unittest.main()

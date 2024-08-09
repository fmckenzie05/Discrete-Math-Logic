# from tries_1 import TrieNode
from ternary import TernaryTree

import csv


# For testing visualization
def visualize(csv_file_path, tree):
    
    # Read words from the CSV file and insert them into the Trie
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0].strip()  # Use strip() to remove any leading/trailing whitespace
            tree.insert(word)

    # Prompt user for input
    prefix = input("Enter a prefix to search for (or leave blank to see the whole Trie): ")

    # Find and display words starting with the given prefix
    results = tree.starts_with(prefix)
    print(f"Words starting with '{prefix}': {results}")

    # Visualize the tree
    tree.visualize(prefix)

def main():
    csv_file_path = '4000-most-common-english-words-csv.csv'

    # Initialize the Trie
    # trie = PrefixTree()
    ternary = TernaryTree()
    visualize(csv_file_path, ternary)

if __name__ == "__main__":
        main()


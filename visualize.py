from tree.tries import PrefixTree
from tree.ternary import TernaryTree

import csv


# For testing visualization
def helper(csv_file_path, tree, prefix):
    
    # Read words from the CSV file and insert them into the Trie
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0].strip()  # Use strip() to remove any leading/trailing whitespace
            tree.insert(word)


    # Find and display words starting with the given prefix
    results = tree.starts_with(prefix)
    print(f"Words starting with '{prefix}': {results}")

    # Visualize the tree
    fig = tree.visualize(prefix)
    print(fig)
    return results, fig

def visualize(csv_file_path='data/4000-most-common-english-words-csv.csv', tree_selection=1, prefix=''):

    # Initialize the Trie
    # trie = PrefixTree()
    if tree_selection == 1:
        tree = PrefixTree()
    elif tree_selection == 2:
        tree = TernaryTree()
    elif tree_selection == 3:
        tree = None

    return helper(csv_file_path, tree, prefix)
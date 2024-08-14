from tree.tries import PrefixTree
from tree.ternary import TernaryTree

import csv


# For testing visualization
def helper(csv_file_path, tree):
    
    # Read words from the CSV file and insert them into the Trie
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            word = row[0].strip()  # Use strip() to remove any leading/trailing whitespace
            tree.insert(word)

    # Prompt user for input
    prefix = input("Enter a prefix to search for (or leave blank to see the whole tree): ")

    # Find and display words starting with the given prefix
    results = tree.starts_with(prefix)
    print(f"Words starting with '{prefix}': {results}")

    # Visualize the tree
    tree.visualize(prefix)
    return results

def visualize(csv_file_path='data/4000-most-common-english-words-csv.csv'):

    # Initialize the Trie
    # trie = PrefixTree()
    print("1. Trie\n2. Ternary\n3. Radix")
    tree_selection = None
    while tree_selection != 1 and tree_selection != 2 and tree_selection != 3:
        tree_selection = int(input("Choose your tree: "))
    
    if tree_selection == 1:
        tree = PrefixTree()
    elif tree_selection == 2:
        tree = TernaryTree()
    elif tree_selection == 3:
        tree = None

    return helper(csv_file_path, tree)





from tree.tries import PrefixTree
from tree.ternary import TernaryTree
from tree.radix import RadixTree

import time

def helper(words, tree, prefix):
    # Measure insertion time
    start_time = time.time()
    for word in words:
        tree.insert(word)
    insertion_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Measure retrieval time
    start_time = time.time()
    results, nodes_traversed = tree.starts_with(prefix)
    retrieval_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Visualize the tree
    fig = tree.visualize(prefix)

    # Get total node count
    total_nodes = tree.size()

    # Return all metrics and results
    return results, fig, nodes_traversed, total_nodes, insertion_time, retrieval_time


def visualize(words, tree_selection=1, prefix=''):
    # Initialize the appropriate tree
    if tree_selection == 1:
        tree = PrefixTree()
    elif tree_selection == 2:
        tree = TernaryTree()
    elif tree_selection == 3:
        tree = RadixTree()
    else:
        raise Exception("Invalid tree selection")

    return helper(words, tree, prefix)

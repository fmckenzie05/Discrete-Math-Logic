# Discrete-Math-Logic

This repository contains a Discrete Math project focused on implementing and visualizing Trie data structures, including Tries, Ternary Search Trees, and Radix Trees. These structures are optimized for efficient string storage and querying, with applications in autocomplete sys,tems, spell checkers, and IP routing.

## Features 
Trie Implementation: Efficiently store and query strings with common prefixes.

Ternary Search Tree: Combine the low space overhead of binary search trees with the character-based efficiency of tries.

Radix Tree: Utilize path compression for reduced memory usage and faster lookups.

Interactive Visualization: Leverage Plotly to visualize the structure and operations of the Trie interactively.


## Technologies
Python
NetworkX
Matplotlib
Plotly

## Tree interface
In the Code folder, we implement classes for Trie, Ternary and Radix tree. Each class have the following methods:
* `insert`: insert a new word to the tree.
* `find`: find and return the node representing the word, or None if it is not found.
* `starts_with`: return a list of all words starting with the given prefix
* `visualize`: visualize the tree with nodes

## How to run
1. Create a virtual env
* Install virtualenv (skip if you already installed it)
```
pip install virtualenv
```
* Create and activate the virtualenv
```
virtualenv myenv

<!-- MacOS/Linux -->
source myenv/bin/activate

<!-- Windows -->
source myenv/bin/activate
```

2. Install libraries / pacakges
```
pip install -r requirements.txt
```

3. Run the application
```
streamlit run app.py
```
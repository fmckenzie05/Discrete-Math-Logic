import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class TrieNode:
    """A node in the Trie structure."""
    def __init__(self, text=''):
        self.text = text
        self.children = dict()
        self.is_word = False

class PrefixTree:
    """A Trie to store and query strings efficiently."""
    
    def __init__(self):
        self.root = TrieNode()
        self.name = "Trie"

    def insert(self, word):
        """Insert a word into the Trie."""
        current = self.root
        for i, char in enumerate(word):
            if char not in current.children:
                prefix = word[0:i+1]
                current.children[char] = TrieNode(prefix)
            current = current.children[char]
        current.is_word = True

    def find(self, word):
        """Find and return the node representing the word, or None if not found."""
        current = self.root
        for char in word:
            if char not in current.children:
                return None
            current = current.children[char]
        return current if current.is_word else None

    def starts_with(self, prefix):
        """Return a list of all words starting with the given prefix."""
        words = list()
        current = self.root
        for char in prefix:
            if char not in current.children:
                return list()
            current = current.children[char]
        self.__child_words_for(current, words)
        return words

    def __child_words_for(self, node, words):
        """Helper method to collect all words under a given node."""
        if node.is_word:
            words.append(node.text)
        for letter in node.children:
            self.__child_words_for(node.children[letter], words)

    def size(self, current=None):
        """Return the total number of nodes in the Trie."""
        if not current:
            current = self.root
        count = 1
        for letter in current.children:
            count += self.size(current.children[letter])
        return count

    def visualize(self, prefix=''):
        """Visualize the Trie using plotly for interactivity."""
        graph = nx.DiGraph()
        current = self.root

        # Start from the given prefix
        for char in prefix:
            if char in current.children:
                current = current.children[char]
            else:
                return  # Prefix not in Trie

        self.__add_nodes(graph, current, "root")

        # Use spring layout for better visualization
        pos = nx.spring_layout(graph)
        edge_x = []
        edge_y = []

        for edge in graph.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.append(x0)
            edge_x.append(x1)
            edge_x.append(None)
            edge_y.append(y0)
            edge_y.append(y1)
            edge_y.append(None)

        edge_trace = go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=0.5, color='#888'),
            hoverinfo='none',
            mode='lines')

        node_x = []
        node_y = []
        labels = []

        for node in graph.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            labels.append(graph.nodes[node].get('label', ''))

        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            text=labels,
            textposition='top center',
            hoverinfo='text',
            marker=dict(
                showscale=False,
                color='skyblue',
                size=10,
                line_width=2))

        fig = go.Figure(data=[edge_trace, node_trace],
                        layout=go.Layout(
                            title=f'Trie Visualization (Prefix: {prefix})',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20,l=5,r=5,t=40),
                            annotations=[dict(
                                text="Trie Visualization",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002 )],
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )
        return fig

    def __add_nodes(self, graph, node, node_id):
        """Helper method to add nodes to the networkx graph."""
        for char, child in node.children.items():
            child_id = node_id + char
            label = f"{char} ({child.text})" if child.is_word else char
            graph.add_node(child_id, label=label)
            graph.add_edge(node_id, child_id)
            self.__add_nodes(graph, child, child_id)

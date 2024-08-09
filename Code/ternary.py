import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Node:
    """A node in the Ternary structure."""
    def __init__(self, data='', left=None, equal=None, right=None, is_end_of_string=False):
        self.data = data
        # Has 3 pointers for left (less), equal (equal), right (greater) - similar to binary tree
        self.left = left
        self.equal = equal
        self.right = right
        # If it's end of String
        self.is_end_of_string = is_end_of_string


class TernaryTree:
    def __init__(self):
        self.root = Node()


    def insert(self, word):
        """Inserts a word into the ternary tree."""
        self.root = self._insert(self.root, word, 0)

    def _insert(self, node, word, index):
        """Helper function to insert a word into the ternary tree."""
        if node is None:
            node = Node(data=word[index])

        if word[index] < node.data:
            node.left = self._insert(node.left, word, index)
        elif word[index] > node.data:
            node.right = self._insert(node.right, word, index)
        else:
            if index + 1 == len(word):
                node.is_end_of_string = True
            else:
                node.equal = self._insert(node.equal, word, index + 1)

        return node

     
    def find(self, word):
        """Find and return the node representing the word, or None if not found."""
        current = self.root
        i = 0

        while i < len(word):
            if word[i] < current.data and current.left:
                current = current.left
            elif word[i] > current.data and current.right:
                current = current.right
            elif word[i] == current.data and current.equal:
                current = current.equal
                i = i + 1
            else:
                return None
                
    def starts_with(self, prefix):
        """Return a list of all words starting with the given prefix."""
        if not prefix:
            prefix = ''
        node = self._search_prefix(self.root, prefix, 0)
        results = []
        if node:
            if node.is_end_of_string:
                results.append(prefix)
            self._collect_words(node.equal, prefix, results)
        return results
        

    def _search_prefix(self, node, prefix, index):
        """Helper function to search for the node that matches the end of the prefix."""
        if node is None:
            return None

        if prefix[index] < node.data:
            return self._search_prefix(node.left, prefix, index)
        elif prefix[index] > node.data:
            return self._search_prefix(node.right, prefix, index)
        else:
            if index + 1 == len(prefix):
                return node
            return self._search_prefix(node.equal, prefix, index + 1)

    def _collect_words(self, node, prefix, results):
        """Helper function to collect all words from a given node."""
        if node is None:
            return

        self._collect_words(node.left, prefix, results)

        if node.is_end_of_string:
            results.append(prefix + node.data)

        self._collect_words(node.equal, prefix + node.data, results)

        self._collect_words(node.right, prefix, results)


    def size(self, current=None):
        """Return the total number of nodes in the Ternary tree"""
        if not current:
            current = self.root
        
        return 1 + self._size(current.left) + self._size(current.equal) + self._size(current.right)
    
    def _size(self, current):
        """Helper function to calculate all nodes from a given node."""
        if not current:
            return 0
        else:
            return 1 + self._size(current.left) + self._size(current.equal) + self._size(current.right)

    # ------------------------------- todo -----------------------------------------
    def visualize(self, prefix=''):
        """Visualize the Ternary tree using plotly for interactivity."""
        graph = nx.DiGraph()
        current = self.root

        # Traverse the tree starting from the given prefix
        for char in prefix:
            if not current:
                return  # Prefix not in Ternary Tree
            if char < current.data:
                current = current.left
            elif char > current.data:
                current = current.right
            else:
                current = current.equal

        self.__add_nodes(graph, current, prefix)

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
                            title=f'Ternary Tree Visualization (Prefix: {prefix})',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Ternary Tree Visualization",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )
        fig.show()

    def __add_nodes(self, graph, node, node_id):
        """Helper method to add nodes to the networkx graph."""
        if node is None:
            return

        # Add the current node
        label = f"{node.data} (End)" if node.is_end_of_string else node.data
        graph.add_node(node_id, label=label)

        # Add left child
        if node.left:
            left_id = node_id + "L"
            graph.add_edge(node_id, left_id)
            self.__add_nodes(graph, node.left, left_id)

        # Add equal child
        if node.equal:
            equal_id = node_id + node.data
            graph.add_edge(node_id, equal_id)
            self.__add_nodes(graph, node.equal, equal_id)

        # Add right child
        if node.right:
            right_id = node_id + "R"
            graph.add_edge(node_id, right_id)
            self.__add_nodes(graph, node.right, right_id)

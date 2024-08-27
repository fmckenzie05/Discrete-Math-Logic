import networkx as nx
import plotly.graph_objects as go

class Node:
    """A node in the Ternary structure."""
    def __init__(self, data='', left=None, equal=None, right=None, is_end_of_string=False):
        self.data = data
        self.left = left
        self.equal = equal
        self.right = right
        self.is_end_of_string = is_end_of_string

class TernaryTree:
    def __init__(self):
        self.root = Node()
        self.name = "Ternary"
        self.traversed_nodes = 0  # Counter for traversed nodes

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
        self.traversed_nodes = 0  # Reset the counter before the search
        current = self.root
        i = 0

        while i < len(word):
            self.traversed_nodes += 1  # Increment the counter for each node visited
            if word[i] < current.data and current.left:
                current = current.left
            elif word[i] > current.data and current.right:
                current = current.right
            elif word[i] == current.data and current.equal:
                current = current.equal
                i += 1
            else:
                return None

        return current if current.is_end_of_string else None

    def starts_with(self, prefix):
        """Return a list of all words starting with the given prefix."""
        self.traversed_nodes = 0  # Reset before each search
        results = []
        if not prefix:
            self._collect_words(self.root, '', results)
            return results, self.traversed_nodes
        
        node = self._search_prefix(self.root, prefix, 0)
        if node:
            if node.is_end_of_string:
                results.append(prefix)
            self._collect_words(node.equal, prefix, results)
        
        return results, self.traversed_nodes

    def _search_prefix(self, node, prefix, index):
        """Helper function to search for the node that matches the end of the prefix."""
        if node is None:
            return None
        self.traversed_nodes += 1  # Increment nodes traversed
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
        """Return the total number of nodes in the Ternary tree."""
        if not current:
            current = self.root
        return 1 + self._size(current.left) + self._size(current.equal) + self._size(current.right)

    def _size(self, current):
        """Helper function to calculate all nodes from a given node."""
        if not current:
            return 0
        else:
            return 1 + self._size(current.left) + self._size(current.equal) + self._size(current.right)

    def visualize(self, prefix=''):
        """Visualizes the ternary tree using NetworkX and Plotly."""
        # Create a directed graph
        graph = nx.DiGraph()

        current = self._search_prefix(self.root, prefix, 0)
        if not current:
            print("Prefix not in tree")
            return
        self.__add_nodes(graph, node=current, node_id="Root")

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
        return fig

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

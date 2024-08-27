import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class RadixNode:
    """A node in the Radix Tree."""
    def __init__(self, text=''):
        self.text = text
        self.children = {}
        self.is_word = False

class RadixTree:
    """A Radix Tree for storing and querying strings efficiently."""
    
    def __init__(self):
        self.root = RadixNode()
        self.name = "Radix"
        self.traversed_nodes = 0 

    def insert(self, word):
        """Insert a word into the Radix Tree, with debug output."""
        current = self.root
        while word:
            found = False
            for char, child in current.children.items():
                common_prefix = self._longest_common_prefix(word, child.text)
                if common_prefix:
                    found = True
                    if common_prefix == child.text:
                        current = child
                        word = word[len(common_prefix):]
                    else:
                        self._split_node(current, child, common_prefix)
                        current = current.children[common_prefix[0]]
                        word = word[len(common_prefix):]
                    break
            if not found:
                new_node = RadixNode(word)
                current.children[word[0]] = new_node
                current = new_node
                word = ''
        current.is_word = True

    def _split_node(self, parent, node, common_prefix):
        # Split the node at the common prefix, adjusting both the node and its new child
        remaining_text = node.text[len(common_prefix):]
        new_child = RadixNode(remaining_text)
        new_child.children = node.children
        new_child.is_word = node.is_word

        node.text = common_prefix
        node.children = {remaining_text[0]: new_child}
        node.is_word = False

        # Ensure the parent's reference to this node is updated if needed
        parent.children[common_prefix[0]] = node


    def _log_tree(self, node, prefix):
        full_word = prefix + node.text
        for child in node.children.values():
            self._log_tree(child, full_word)

    def _longest_common_prefix(self, word1, word2):
        min_len = min(len(word1), len(word2))
        for i in range(min_len):
            if word1[i] != word2[i]:
                return word1[:i]
        return word1[:min_len]

    def _collect_words(self, node, accumulated_prefix, results, original_prefix=''):

        if node.is_word:
            full_word = accumulated_prefix + node.text
            results.append(full_word)

        for child_char, child in node.children.items():
            if original_prefix and child_char == original_prefix[0]:
                new_accumulated_prefix = accumulated_prefix + child.text
                new_original_prefix = original_prefix[1:]
            else:
                # Only accumulate if we're on the original prefix path AND the current node is NOT a word-ending node
                # Also, don't accumulate if the original_prefix is empty 
                if original_prefix and not node.is_word and original_prefix != child_char: 
                    new_accumulated_prefix = accumulated_prefix + child_char
                else:
                    new_accumulated_prefix = accumulated_prefix
                new_original_prefix = '' if original_prefix else original_prefix

            self._collect_words(child, new_accumulated_prefix, results, new_original_prefix)



    def starts_with(self, prefix):
        self.traversed_nodes = 0  # Reset before each search
        current = self.root
        path_to_current = ''
        original_prefix = prefix
        
        while prefix:
            found = False
            for child in current.children.values():
                self.traversed_nodes += 1  # Increment nodes traversed
                if prefix.startswith(child.text):
                    path_to_current += child.text
                    current = child
                    prefix = prefix[len(child.text):]
                    found = True
                    break
            if not found:
                return [], self.traversed_nodes  # No match found, return empty list and nodes traversed

        results = []
        self._collect_words(current, path_to_current, results, original_prefix)
        return results, self.traversed_nodes 



    def visualize(self, prefix=''):
        graph = nx.DiGraph()
        current = self.root
        while prefix:
            found = False
            for child in current.children.values():
                if prefix.startswith(child.text):
                    current = child
                    prefix = prefix[len(child.text):]
                    found = True
                    break
            if not found:
                return

        self._add_nodes(graph, current, "root")
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
                            title=f'Radix Tree Visualization (Prefix: {prefix})',
                            titlefont_size=16,
                            showlegend=False,
                            hovermode='closest',
                            margin=dict(b=20, l=5, r=5, t=40),
                            annotations=[dict(
                                text="Radix Tree Visualization",
                                showarrow=False,
                                xref="paper", yref="paper",
                                x=0.005, y=-0.002)],
                            xaxis=dict(showgrid=False, zeroline=False),
                            yaxis=dict(showgrid=False, zeroline=False))
                        )
        return fig

    def _add_nodes(self, graph, node, node_id):
        for child in node.children.values():
            child_id = node_id + child.text  # Ensure unique node IDs
            label = f"{child.text} ({'Word' if child.is_word else 'Prefix'})"
            graph.add_node(child_id, label=label)
            graph.add_edge(node_id, child_id)
            self._add_nodes(graph, child, child_id)

    def size(self, current=None):
        """Return the total number of nodes in the Radix Tree."""
        if not current:
            current = self.root
        return 1 + sum(self.size(child) for child in current.children.values())
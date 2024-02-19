# src/pygame/models/table.py
from .node import Node  # Import the Node class

class Table:
    def __init__(self, node_radius):
        self.nodes = []
        self.node_radius = node_radius

    def addNode(self, node):
        self.nodes.append(node)

    def _create_nodes(self, count, radius):
        """Initialize nodes with dummy positions. You'll need to update this to position nodes correctly."""
        nodes = []
        for i in range(count):
            # Placeholder position (x, y). You should replace this with your actual layout logic.
            position = (50 * (i % 10), 50 * (i // 10))
            nodes.append(Node(position, radius))
        return nodes

    # Add more methods as needed for table-wide behavior, like animations or updates from API data

import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the diagram from JSON file
def load_diagram(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

# Build the graph from the diagram data
def build_graph(diagram):
    G = nx.DiGraph()
    for node in diagram["nodes"]:
        G.add_node(node["id"], node_type=node["type"], text=node["text"])
    for edge in diagram["edges"]:
        G.add_edge(edge["from"], edge["to"], condition=edge.get("condition", ""))
    return G

# Generate a simple top-to-bottom layout
def top_to_bottom_layout(G):
    layers = {}  # Dictionary to store nodes at each layer
    visited = set()

    # Perform BFS (Breadth-First Search) to determine levels
    def bfs(start_node):
        queue = [(start_node, 0)]  # (node, level)
        while queue:
            node, level = queue.pop(0)
            if node not in visited:
                visited.add(node)
                if level not in layers:
                    layers[level] = []
                layers[level].append(node)
                for neighbor in G.successors(node):
                    queue.append((neighbor, level + 1))

    # Assume 'start' node is the root
    start_node = next((n for n, d in G.nodes(data=True) if d['node_type'] == 'start'), None)
    if start_node:
        bfs(start_node)

    # Assign positions for nodes based on their layer
    pos = {}
    y_gap = 2  # Vertical spacing
    x_gap = 2  # Horizontal spacing within a layer
    for layer, nodes in layers.items():
        x_start = -(len(nodes) - 1) * x_gap / 2  # Center nodes horizontally
        for i, node in enumerate(nodes):
            pos[node] = (x_start + i * x_gap, -layer * y_gap)  # (x, y)

    return pos

# Visualize the flowchart
def visualize_flowchart(G):
    # Generate custom top-to-bottom positions
    pos = top_to_bottom_layout(G)

    # Get node attributes for labels
    labels = nx.get_node_attributes(G, 'text')

    # Draw the graph
    plt.figure(figsize=(10, 12))
    nx.draw(
        G, pos,
        with_labels=True,
        labels=labels,
        node_size=4000,
        node_color="skyblue",
        font_size=10,
        font_weight="bold",
        edge_color="gray",
        arrows=True
    )

    # Draw edge labels (e.g., conditions)
    edge_labels = nx.get_edge_attributes(G, 'condition')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=18)

    # Title and display
    plt.title("Top-to-Bottom Flowchart Visualization (NetworkX)", fontsize=16)
    plt.tight_layout()
    plt.show()

# Main function
def main():
    file_path = "diagram.json"  # Ensure diagram.json is in the same folder
    diagram = load_diagram(file_path)
    G = build_graph(diagram)
    visualize_flowchart(G)

if __name__ == "__main__":
    main()

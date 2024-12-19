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

    # Add nodes
    for node in diagram["nodes"]:
        G.add_node(node["id"], node_type=node["type"], text=node["text"])

    # Add edges
    for edge in diagram["edges"]:
        G.add_edge(edge["from"], edge["to"], condition=edge.get("condition", ""))

    return G

# Visualize the flowchart
def visualize_flowchart(G):
    # Create a layout for the graph
    pos = nx.planar_layout(G)  # You can experiment with spring_layout, shell_layout, etc.

    # Get node attributes for labels
    labels = nx.get_node_attributes(G, 'text')

    # Draw the graph
    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        labels=labels,
        node_size=3000,
        node_color='lightblue',
        font_size=10,
        font_weight='bold',
        edge_color='gray'
    )

    # Draw edge labels (e.g., conditions)
    edge_labels = nx.get_edge_attributes(G, 'condition')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Show the plot
    plt.title("Flowchart Visualization", fontsize=16)
    plt.show()

# Main function
def main():
    # Load the diagram
    file_path = "diagram.json"  # Ensure diagram.json is in the same folder as this script
    diagram = load_diagram(file_path)

    # Build the graph
    G = build_graph(diagram)

    # Visualize the flowchart
    visualize_flowchart(G)

if __name__ == "__main__":
    main()

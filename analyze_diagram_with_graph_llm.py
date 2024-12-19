import json
import re
import networkx as nx
from genai_api import gemini_api_response_diagram_analysis
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")



# Load the diagram from JSON file
with open("diagram.json", "r") as f:
    diagram = json.load(f)

nodes = diagram["nodes"]
edges = diagram["edges"]

G = nx.DiGraph()

# Add nodes and edges
for node in nodes:
    G.add_node(node["id"], node_type=node["type"], text=node["text"])

for edge in edges:
    G.add_edge(edge["from"], edge["to"], condition=edge.get("condition"))

# Identify start and end nodes
start_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'start']
end_nodes = [n for n, d in G.nodes(data=True) if d['node_type'] == 'end']

structural_score = 100

# Check structural correctness
if len(start_nodes) != 1:
    print("Error: There should be exactly one start node.")
    structural_score = 0

if len(end_nodes) != 1:
    print("Error: There should be exactly one end node.")
    structural_score = 0

if structural_score == 100:
    start = start_nodes[0]
    reachable = nx.descendants(G, start) | {start}
    for n in G.nodes:
        if n not in reachable:
            print(f"Node {n} is not reachable from the start node.")
            structural_score = 0
    for end in end_nodes:
        if end not in reachable:
            print(f"End node {end} is not reachable from the start node.")
            structural_score = 0

print("Structural Score:", structural_score)

# Extract node texts for LLM evaluation
try:
    ordered_nodes = list(nx.topological_sort(G))
except nx.NetworkXUnfeasible:
    if structural_score == 100 and start_nodes:
        start = start_nodes[0]
        ordered_nodes = list(nx.dfs_preorder_nodes(G, start))
    else:
        ordered_nodes = list(G.nodes)

node_texts = [G.nodes[n]['text'] for n in ordered_nodes]
combined_text = " -> ".join(node_texts)

prompt = f"""
You are a tutor checking a student's flowchart. 
The student's flowchart sequence of steps is:
{combined_text}

The expected solution is a loop from 0 to 9 printing each number.
Does the student's description match the logic of printing numbers from 0 to 9 in a loop?
Give a brief justification and a final score from 0 to 100.
"""

response = gemini_api_response_diagram_analysis(prompt)

evaluation_text = response
def extract_score(evaluation_text):
    # Match "Score: X" or "X/100" patterns
    match = re.search(r"Score[:\s]*([0-9]+)", evaluation_text)
    if match:
        return int(match.group(1))

    # Fallback for "X/100" pattern
    match = re.search(r"([0-9]+)/100", evaluation_text)
    if match:
        return int(match.group(1))

    # Default score if no valid pattern is found
    return 50

# Extract and display the score
semantic_score = extract_score(evaluation_text)
print("Semantic Score:", semantic_score)

# Combine with structural score
structural_score = 100  # Assume structural checks passed
final_score = 0.6 * structural_score + 0.4 * semantic_score
print("Final Combined Score:", final_score)
print(response)

if structural_score < 100:
    print("Feedback: Check your flowchart structure. Ensure a single start and end node and proper connectivity.")

if semantic_score < 100:
    print("Feedback: The logic could be improved. Ensure that your steps match the intended algorithm more closely.")

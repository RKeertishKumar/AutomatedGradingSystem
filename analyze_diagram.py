import re
from genai_api import gemini_api_response_diagram_analysis

# Placeholder for the node text processing
node_texts = ["Step 1: Initialize loop", "Step 2: Condition check", "Step 3: Increment", "Step 4: Print"]
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
print(response)
if semantic_score < 100:
    print("Feedback: The logic could be improved. Ensure that your steps match the intended algorithm more closely.")

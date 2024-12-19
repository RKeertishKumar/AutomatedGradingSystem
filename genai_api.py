import google.generativeai as genai
import os

def clean_response(response):
    if response.startswith("```python"):
        response = response[len("```python"):].strip()
    if response.endswith("```"):
        response = response[:-len("```")].strip()
    return response

def gemini_api_response(resume_info,path_info):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(f"Roadmap for {path_info} role in 5 points based on weakness in {resume_info}. Also, 3 interview question and answer.")
    suggesetion = response.text
    return suggesetion

def gemini_api_response_job_role(resume_info,path_info,job_role):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(f"Roadmap for {path_info} role in 5 points based on weakness in {resume_info} for {job_role}.Also, 3 interview question and answer.")
    suggesetion = response.text
    return suggesetion

def gemini_api_flashcards(text):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(f"give only a python list with 5 important interview question and answers for topics within {text} in this format with question as key and answer as value with a list of dictionaries")
    suggesetion = response.text
    suggesetion = clean_response(suggesetion)
    return suggesetion

def gemini_api_response_diagram_analysis(prompt):
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])

    model = genai.GenerativeModel('gemini-1.5-flash')

    response = model.generate_content(prompt)
    suggesetion = response.text
    return suggesetion
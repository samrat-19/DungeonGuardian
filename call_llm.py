import requests

# Please store credentials in env file. This is strictly for demo purpose
API_URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

def call_llm(prompt, max_retries=3):
    """Generic function to call LLM API with retries."""
    body = {"model": "llama3.1", "prompt": prompt, "stream": False}

    for _ in range(max_retries):
        response = requests.post(API_URL, json=body, headers=HEADERS)
        if response.status_code == 200:
            return response.json().get("response", "")

    return ""  # Return empty string if all retries fail
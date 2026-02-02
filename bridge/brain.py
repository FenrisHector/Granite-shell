import sys
import requests
import re

# Configuration
MODEL_ID = "granite-code"
API_URL = "http://localhost:11434/api/generate"

def get_command(user_prompt):
    # Prompt strategy: Ask for a single command
    payload = {
        "model": MODEL_ID,
        "prompt": f"Write a single linux command to: {user_prompt}",
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    try:
        # Send the request to the local LLM server and extract the raw text
        response = requests.post(API_URL, json=payload)
        response.raise_for_status() # Raises an error if HTTP status is 4xx or 5xx
        raw_text = response.json()['response']

        # Extract command from code block if present
        code_match = re.search(r"```(?:bash|sh)?\s*(.*?)\s*```", raw_text, re.DOTALL)

        if code_match:
            command = code_match.group(1).strip()
        else:
            # If no code block, take raw text and remove inline backticks
            command = raw_text.strip()
            if command.startswith("`"):
                command = command.replace("`", "")

        # Only return the first line to prevent multi-line malicious scripts
        return command.split('\n')[0]

    except Exception as e:
        # In case of error, return a safe echo command
        return f"echo 'Error: {str(e)}'"

if __name__ == "__main__":
    # Read arguments passed from the C program
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(get_command(prompt)) # Print to stdout so C can read it via pipe
    else:
        print("echo 'Error: No input provided'")

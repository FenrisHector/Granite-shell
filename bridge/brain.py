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
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        raw_text = response.json()['response']

        # Search for markdown code blocks
        code_match = re.search(r"```(?:bash|sh)?\s*(.*?)\s*```", raw_text, re.DOTALL)

        if code_match:
            command = code_match.group(1).strip()
        else:
            command = raw_text.strip()
            if command.startswith("`"):
                command = command.replace("`", "")

        return command.split('\n')[0]

    except Exception as e:
        return f"echo 'Error: {str(e)}'"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
        print(get_command(prompt))
    else:
        print("echo 'Error: No input provided'")

import requests
from dotenv import load_dotenv
import os
from pprint import pprint

# Load environment variables
load_dotenv()
IOINTELLIGENCE_API_KEY = os.getenv("API_KEY_IONET")

# Define headers and URL
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {IOINTELLIGENCE_API_KEY}",
}
url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

# Define system prompt and message payload
system_prompt = """
You are a competitive chess engine playing as Black against a master-level opponent.

Your task is to respond with exactly one legal move in UCI format based on the full move history: {moves}.

Rules:

Follow all official chess rules.

Do not repeat any previous move.

Do not move from an empty square.

Do not make illegal moves.

Any illegal move results in immediate loss.

Do not explain, comment, or add any extra text.

Output: Return only one move in UCI format (e.g., e7e5, g8f6, a7a5). No extra text. No formatting. No commentary. No punctuation.

Play with precision. Play sharp. Play by the rules.
"""
while True:
    with open("moves.txt", "r") as file:
        moves = file.read()
    system_formated_prompt = system_prompt.format(moves = moves)
    user = input("whats your move?: ")
    data = {
        "model": "mistralai/Mistral-Large-Instruct-2411",
        "messages": [
            {
                "role": "system",
                "content": system_formated_prompt
            },
            {
                "role": "user",
                "content": user
            }
        ]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Parse the response
    res = response.json()
    content = res['choices'][0]['message']['content'].strip()

# Print result based on content
    if "mate" in user:
        print("game over")
        with open("moves.txt", "w") as file:
            file.write("")
        break
    else:
        print(content)
        move = f"oponent move:{user}, player move:{content}\n"
        with open("moves.txt", "a") as file:
            file.write(move)


from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json



app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# read assistant_config.json
with open('assistant_config.json', 'r') as config_file:
    config = json.load(config_file)

conversation_history = []

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    global conversation_history
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    # add userinput into history
    conversation_history.append({"role": "user", "content": user_input})

    # Send the conversation history to OpenAI's API to maintain context
    response = openai.ChatCompletion.create(
        model=config["model"],
        messages=[
            {"role": "system", "content": config["system_instruction"]},
            {"role": "user", "content": user_input}
        ]+ conversation_history,
        max_tokens=config["max_tokens"],
        temperature=config["temperature"]
    )

    answer = response.choices[0].message["content"].strip()

    # add answer from assistant into history
    conversation_history.append({"role": "assistant", "content": answer})

    return jsonify({"answer": answer})


# reset conversation history
@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({"message": "Conversation history reset."})

# Vocabulary route to fetch word definition and example
@app.route("/vocabulary", methods=["POST"])
def get_vocabulary():
    data = request.json
    word = data.get('word')

    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Mock response with definition and example
    # Replace this with a call to a dictionary API if available
    mock_response = {
        "word": word,
        "definition": f"{word} is a sample definition.",
        "example": f"This is an example sentence using {word}."
    }

    return jsonify(mock_response)

if __name__ == "__main__":
    app.run(debug=True)

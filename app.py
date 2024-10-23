from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    user_input = data.get('message')

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = openai.Completion.create(
        model="gpt-4",  # or "gpt-3.5-turbo"
        prompt=user_input,
        max_tokens=150,
        temperature=0.7
    )

    answer = response.choices[0].text.strip()
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

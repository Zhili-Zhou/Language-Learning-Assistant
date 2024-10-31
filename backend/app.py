from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json
from gtts import gTTS
from io import BytesIO
import random


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

        # Generate audio response using gTTS
    tts = gTTS(answer, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Return both the text and audio as a response
    return jsonify({
        "answer": answer,
        "audio": audio_file.getvalue().decode('latin1')
    })


@app.route("/pronounce", methods=["POST"])
def pronounce():
    data = request.json
    word = data.get('word')

    if not word:
        return jsonify({"error": "No word provided"}), 400

    # Generate pronunciation using gTTS
    tts = gTTS(word, lang='en')
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)

    # Send the audio file as response
    return send_file(audio_file, mimetype="audio/mp3", as_attachment=False, download_name="pronunciation.mp3")


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

# Daily word route to provide a word, definition, and examples
@app.route("/daily_word", methods=["GET"])
def daily_word():
    # Mock vocabulary words for demonstration purposes
    words = [
        {
            "word": "elucidate",
            "meaning": "To make something clear or to explain.",
            "examples": ["Please elucidate your point.", "The teacher elucidated the topic with ease."]
        },
        {
            "word": "gregarious",
            "meaning": "Fond of company; sociable.",
            "examples": ["Sheep are very gregarious animals.", "He was a gregarious person who enjoyed large gatherings."]
        },
        {
            "word": "persevere",
            "meaning": "To continue in a course of action even in the face of difficulty.",
            "examples": ["She persevered through the challenges.", "He persevered despite numerous setbacks."]
        }
    ]

    # Select a random word from the list
    daily_word_data = random.choice(words)
    
    return jsonify(daily_word_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

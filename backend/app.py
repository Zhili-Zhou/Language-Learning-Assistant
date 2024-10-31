from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv
import json
from gtts import gTTS
from io import BytesIO
import re
import base64
from PIL import Image


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# read assistant_config.json
with open('assistant_config.json', 'r') as config_file:
    config = json.load(config_file)

conversation_history = []
roleplay_conversation_history =[]


# Load OpenAI API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")



'''----------------------------normal text assistant------------------------------------'''

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

    # Return both the text and audio as a response
    return jsonify({"answer": answer})

LANGUAGE_CODES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Chinese": "zh",
    "Japanese": "ja"
}

# Endpoint to generate pronunciation audio
@app.route("/pronounce", methods=["POST"])
def pronounce():
    data = request.json
    text = data.get("text")  
    language_name = data.get("language", "English") 
    language_code = LANGUAGE_CODES.get(language_name, "en")  # Default to English if language is not recognized


    if not text:
        return jsonify({"error": "No word provided"}), 400

    try:
        # Generate speech using gTTS
        tts = gTTS(text=text, lang=language_code)
        filename = "pronunciation.mp3"
        tts.save(filename)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": f"Failed to generate pronunciation: {str(e)}"}), 500
    

#reset chat history
@app.route("/reset_chat", methods=["POST"])
def reset_chat():
    global conversation_history 
    conversation_history = []
    return jsonify({"message": "Conversation history reset."})
    
    
'''----------------------------roleplay assistant------------------------------------'''


def is_image_request(message):
    # Check if the message is likely to be an image request
    keywords = ["show me", "picture of", "what is", "how does"]
    return any(keyword in message.lower() for keyword in keywords)


@app.route("/roleplay", methods=["POST"])
def roleplay():
    global roleplay_conversation_history
    data = request.json
    user_message = data.get("message")
    language = data.get("language", "English")  # Default to English if no language specified
    scenario = data.get("scenario", "restaurant")  # Default to "restaurant" if no scenario specified

    if not user_message:
        return jsonify({"error": "No input provided"}), 400
    
    roleplay_conversation_history.append({"role": "user", "content": user_message})

    

    # Constructing a scenario-specific prompt
    prompt = f"You are a language learning assistant helping a user practice {language}. The scenario is '{scenario}'. \
    Engage in a conversation as if you were in this situation, responding in {language} with the correct phrases. \
    If the user makes any language mistakes, kindly correct them and provide the right response. \
    Here is the user's message: '{user_message}'\
    Be more active into the conversation, make it easier for the user to continue talking and learning.\
    "


    # Check if this message is confirming an image request
    if  is_image_request(user_message.lower()):
        try:
            # Use DALL-E to generate an image based on the user's request
            image_response = openai.Image.create(
                prompt=user_message,
                n=1,
                size="256x256"
            )
            image_url = image_response['data'][0]['url']
            answer = "Here is the image you requested:"
            return jsonify({"answer": answer, "image_url": image_url})
        except Exception as e:
            return jsonify({"error": f"Image generation failed: {str(e)}"}), 500

    else: 

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user_message}
            ]+ roleplay_conversation_history,
            max_tokens=150,
            temperature=0.7
        )

        answer = response.choices[0].message['content'].strip()

        # Add answer into memory
        roleplay_conversation_history.append({"role": "assistant", "content": answer})

        return jsonify({"answer": answer})
    
# Reset roleplay history route
@app.route("/reset_roleplay", methods=["POST"])
def reset_roleplay():
    global roleplay_conversation_history
    roleplay_conversation_history = []
    return jsonify({"message": "Roleplay history reset."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def ask_assistant(question):
    response = openai.Completion.create(
        model="gpt-4",
        prompt=question,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    user_input = input("Ask the Assistant: ")
    print(ask_assistant(user_input))

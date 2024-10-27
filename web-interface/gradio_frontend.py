import gradio as gr
import requests

# URL of your Flask backend
BACKEND_URL = "http://127.0.0.1:5000"  

# Function to send user input to Flask backend
def ask_backend(user_input):
    response = requests.post(f"{BACKEND_URL}/ask", json={"message": user_input})
    if response.status_code == 200:
        return response.json()["answer"]
    else:
        return "Error communicating with the assistant."

# Function to reset the conversation
def reset_backend():
    response = requests.post(f"{BACKEND_URL}/reset")
    return response.json()["message"]

# Create function to handle chat input/output
def chat_with_memory(chat_history, user_input):
    if user_input == "/reset":
        reset_backend()
        return [], "Conversation reset."
    
    # Get the assistant's response
    assistant_reply = ask_backend(user_input)
    
    # Append to chat history and return
    chat_history.append((user_input, assistant_reply))
    return chat_history, ""

# Function to clear the history when reset is clicked
def clear_conversation():
    reset_backend()
    return [], ""


# Set up Gradio Chatbot Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 Your Language Assistant")
    chatbot = gr.Chatbot(label="Chat with Assistant")
    with gr.Row():
        with gr.Column(scale=10):
            user_input = gr.Textbox(placeholder="Ask me something", container=False, scale=10)
        with gr.Column(scale=1):
            send_button = gr.Button("💬 send")
        reset_button = gr.Button("🔄 Reset Conversation")
    
    # Link the buttons to functions
    send_button.click(chat_with_memory, [chatbot, user_input], [chatbot, user_input], queue=False)
    reset_button.click(clear_conversation, [], [chatbot, user_input], queue=False)

if __name__ == "__main__":
    demo.launch(share=True)

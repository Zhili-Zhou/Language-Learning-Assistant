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

# Function to reset the chat conversation
def reset_backend():
    response = requests.post(f"{BACKEND_URL}/reset")
    return response.json()["message"]

# Create function to handle chat input/output
def chat_with_memory(chat_history, user_input):
    if user_input == "/reset":
        reset_backend()
        return [], "Conversation reset."
    
    assistant_reply = ask_backend(user_input)
    chat_history.append((user_input, assistant_reply))
    return chat_history, ""

# Function to clear the history when reset is clicked
def clear_conversation():
    reset_backend()
    return []

def get_pronunciation(word, language):
    response = requests.post(f"{BACKEND_URL}/pronounce", json={"text": word, "language": language})
    if response.status_code == 200:
        with open("pronunciation.mp3", "wb") as f:
            f.write(response.content)
        return "pronunciation.mp3"
    else:
        return "Error: Could not generate pronunciation."
    
# Roleplay function
def roleplay_with_memory(roleplay_history, user_input, language, scenario):
    response = requests.post(f"{BACKEND_URL}/roleplay", json={"message": user_input, "language": language, "scenario": scenario})
    data = response.json()
    answer = data.get("answer", "Error communicating with the assistant.")
    image_url = data.get("image_url")
    
    roleplay_history.append((user_input, answer))
    if image_url:
        roleplay_history.append(("Assistant", f"{answer} <img src='{image_url}' width='256' height='256'>"))
    return roleplay_history, ""

# Set up Gradio Chatbot Interface
with gr.Blocks() as demo:
    gr.Markdown("""
    # 🧠 Language Learning Assistant
    **Welcome to the Language Learning Assistant!**\n
    Explore various language features such as translations, grammar explanations, pronunciation practice, and roleplay scenarios!
    """)

    with gr.Tabs():
        # Chat Tab
        with gr.Tab("Chat"):
            gr.Markdown("""
            Tell the assistant what kind of language you want to learn and start your learning journey.
            Here are some ways you can use this assistant:
            - 💬 **Ask for translations**, e.g., "How do I say 'Good Morning' in French?"
            - 📚 **Get grammar explanations**, e.g., "Can you explain how to use the German dative case?"
            - 🗣️ **Practice pronunciation**, just type in the word you want to know how to pronounce!
            - ✨ **Clear the conversation memory**, just lick "🔄 Reset Conversation".
            - 📖 **Daily Vocabulary Word**: eg. " Give me some german words about food."
                 """)
            chat_history = gr.State([])
            chat_interface = gr.Chatbot(label="Chat with Assistant")
            user_input = gr.Textbox(placeholder="Ask me something", label="Your Message", lines=1)  # Remove `enter=True`
            submit_button = gr.Button("💬 Send")
            reset_button = gr.Button("🔄 Reset Conversation")

            # Trigger chat function with "Enter" key and button click
            user_input.submit(chat_with_memory, inputs=[chat_history, user_input], outputs=[chat_interface, user_input])
            submit_button.click(chat_with_memory, inputs=[chat_history, user_input], outputs=[chat_interface, user_input])
            reset_button.click(clear_conversation, outputs=chat_interface)

            gr.Markdown("## Ask for Pronunciation")
            word_input = gr.Textbox(label="Enter something to pronounce:")
            language_dropdown = gr.Dropdown(["English", "French", "German", "Spanish", "Italian", "Chinese", "Japanese"], label="Choose Language")
            pronunciation_button = gr.Button("Pronounce")
            pronunciation_audio = gr.Audio(label="Pronunciation", type="filepath")

            pronunciation_button.click(get_pronunciation, inputs=[word_input, language_dropdown], outputs=pronunciation_audio)

        # Roleplay Tab
        with gr.Tab("Roleplay"):
            gr.Markdown("""
            ## Roleplay Instructions
            In this Roleplay section, you can practice conversational scenarios in your chosen language! 
            1. **Select a language and scenario** from the dropdowns.
            2. **Type your message** to interact with the assistant, as if you're in the chosen scenario.
            3. If you encounter something you don't understand, simply type **"show me the picture of..."** followed by what you need to visualize, and the assistant will display an image to help.
            4. Use the **Reset Conversation** button to start fresh anytime!
            
            Enjoy your roleplay practice!
            """)
            roleplay_history = gr.State([])
            language = gr.Dropdown(["English", "German", "French", "Spanish"], label="Select Language", interactive=True)
            scenario = gr.Dropdown(["restaurant", "hotel check-in", "shopping", "ordering a taxi"], label="Select Scenario", interactive=True)
            roleplay_interface = gr.Chatbot(label="Roleplay Chatbox", show_label=False)
            roleplay_input = gr.Textbox(placeholder="Enter your message", label="Your Message", lines=1)  # Remove `enter=True`
            roleplay_submit_button = gr.Button("💬 Send")
            roleplay_reset_button = gr.Button("🔄 Reset Conversation")

            # Trigger roleplay function with "Enter" key and button click
            roleplay_input.submit(roleplay_with_memory, inputs=[roleplay_history, roleplay_input, language, scenario], outputs=[roleplay_interface, roleplay_input])
            roleplay_submit_button.click(roleplay_with_memory, inputs=[roleplay_history, roleplay_input, language, scenario], outputs=[roleplay_interface, roleplay_input])
            roleplay_reset_button.click(clear_conversation, outputs=roleplay_interface)

if __name__ == "__main__":
    demo.launch(share=True)


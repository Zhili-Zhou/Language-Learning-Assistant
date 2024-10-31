import gradio as gr
import requests

# Placeholder backend URL
BACKEND_URL = "http://127.0.0.1:5000"

# Placeholder functions for testing
def chat_with_memory(chat_history, user_input):
    chat_history.append((user_input, "This is a placeholder response."))
    return chat_history, ""

def clear_chat_conversation(chat_history):
    chat_history.clear()
    return gr.update(value=[])

def roleplay_with_memory(roleplay_history, user_input, language, scenario):
    roleplay_history.append((user_input, "This is a placeholder roleplay response."))
    return roleplay_history, ""

def get_pronunciation(word, language):
    # Placeholder for pronunciation audio file path
    return "/path/to/pronunciation.mp3"

def get_daily_word():
    # Placeholder daily word response
    return "Word: example\nMeaning: a placeholder word\nExamples:\n- This is an example sentence."

# Gradio Interface
with gr.Blocks(css="""
    /* Custom CSS for styling */
    .tab-container button {
        text-decoration: none;
    .gradio-container .tab-container {
        background-color: #f0f0f0;
        padding: 10px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
""") as demo:
    gr.Markdown("""
    # 🧠 Language Learning Assistant
    **Welcome to the Language Learning Assistant!**  
    Explore various language features such as translations, grammar explanations, pronunciation practice, and roleplay scenarios!
    """)

    with gr.Tabs():
        # Chat Tab
        with gr.Tab("Chat"):
            gr.Markdown("""
            Tell the assistant what kind of language you want to learn and start your learning journey. Here are some ways you can use this assistant:
            - 💬 **Ask for translations**, e.g., "How do I say 'Good Morning' in French?"
            - 📚 **Get grammar explanations**, e.g., "Can you explain how to use the German dative case?"
            - 🗣️ **Practice pronunciation**, just type in the word you want to know how to pronounce!
            - ✨ **Clear the conversation memory**, just click "🔄 Reset Conversation".
            - 📖 **Daily Vocabulary Word**: eg. "Give me some German words about food."
            """)

            chat_history = gr.State([])
            chat_interface = gr.Chatbot(label="Chat with Assistant")
            user_input = gr.Textbox(placeholder="Ask me something", label="Your Message", lines=1)
            submit_button = gr.Button("💬 Send")
            reset_button = gr.Button("🔄 Reset Conversation")

            user_input.submit(chat_with_memory, inputs=[chat_history, user_input], outputs=[chat_interface, user_input])
            submit_button.click(chat_with_memory, inputs=[chat_history, user_input], outputs=[chat_interface, user_input])
            reset_button.click(clear_chat_conversation, inputs=[chat_history], outputs=chat_interface)

            gr.Markdown("### Daily Vocabulary Word")
            daily_word_button = gr.Button("Get Daily Word")
            daily_word_output = gr.Textbox(label="Today's Word with Meaning and Examples:", lines=5)
            daily_word_button.click(get_daily_word, outputs=daily_word_output)

            # Pronunciation
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
            2. **Type your message** to interact with the assistant as if you're in the chosen scenario.
            3. If you encounter something you don't understand, type **"show me the picture of..."** followed by what you need to visualize, and the assistant will display an image to help.
            4. Use the **Reset Conversation** button to start fresh anytime!

            Enjoy your roleplay practice!
            """)

            roleplay_history = gr.State([])
            language = gr.Dropdown(["English", "German", "French", "Spanish"], label="Select Language", interactive=True)
            scenario = gr.Dropdown(["restaurant", "hotel check-in", "shopping", "ordering a taxi"], label="Select Scenario", interactive=True)
            roleplay_interface = gr.Chatbot(label="Roleplay Chatbox", show_label=False)
            roleplay_input = gr.Textbox(placeholder="Enter your message", label="Your Message", lines=1)
            roleplay_submit_button = gr.Button("💬 Send")
            roleplay_reset_button = gr.Button("🔄 Reset Conversation")

            roleplay_input.submit(roleplay_with_memory, inputs=[roleplay_history, roleplay_input, language, scenario], outputs=[roleplay_interface, roleplay_input])
            roleplay_submit_button.click(roleplay_with_memory, inputs=[roleplay_history, roleplay_input, language, scenario], outputs=[roleplay_interface, roleplay_input])
            roleplay_reset_button.click(clear_chat_conversation, inputs=[roleplay_history], outputs=roleplay_interface)

if __name__ == "__main__":
    demo.launch(share=True)

# Import necessary libraries
import google.generativeai as genai
import os
import sys

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual Gemini API key.
# It's highly recommended to load this from an environment variable for security.
# For example, you can set it as: export GOOGLE_API_KEY='your_api_key_here'
# in your terminal, or add it to your .bashrc/.zshrc file.
# If you don't have an API key, you can get one from Google AI Studio:
# https://aistudio.google.com/app/apikey

# Attempt to get the API key from an environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    print("Please set your API key before running the script.")
    print("Example: export GOOGLE_API_KEY='your_api_key_here'")
    sys.exit(1) # Exit if API key is not found

# Configure the generative AI model with your API key
genai.configure(api_key=API_KEY)

# --- Model Initialization ---
# Initialize the generative model.
# The previous error indicated 'gemini-pro' was not found or supported for generateContent.
# Let's try 'gemini-1.5-flash' or 'gemini-1.0-pro' as they are often more widely available.
# You can uncomment one of the lines below and comment out the other.
model = genai.GenerativeModel('gemini-1.5-flash') # Recommended: Fast and cost-effective
# model = genai.GenerativeModel('gemini-1.0-pro') # Alternative: Powerful general-purpose model


# Start a new chat session.
# This keeps track of the conversation history for a more coherent dialogue.
chat = model.start_chat(history=[])

# --- Chatbot Functions ---

def get_bot_response(user_message):
    """
    Sends the user's message to the Gemini model and returns the bot's response.
    Includes basic error handling for API calls.
    """
    try:
        # Send the message and get the response from the model
        response = chat.send_message(user_message)
        # Return the text content of the response
        return response.text
    except Exception as e:
        # Print any errors that occur during the API call
        return f"Error: Could not get a response from the bot. Details: {e}"

def main():
    """
    Main function to run the chatbot in a loop.
    It continuously prompts the user for input and displays the bot's response.
    """
    print("Welcome to the Python Chatbot! (Type 'exit' or 'quit' to end the chat)")
    print("-" * 50)

    while True:
        # Get user input
        user_input = input("You: ")

        # Check for exit commands
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        # Get bot response
        bot_response = get_bot_response(user_input)

        # Display bot response
        print(f"Bot: {bot_response}")
        print("-" * 50)

# --- Run the Chatbot ---
if __name__ == "__main__":
    main()

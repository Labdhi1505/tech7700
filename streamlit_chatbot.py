import streamlit as st
import google.generativeai as genai
import os
import datetime
import pytz
import time 
import random 

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("Error: GOOGLE_API_KEY environment variable not set.")
    st.warning("Please set your API key before running the app. Example: export GOOGLE_API_KEY='your_api_key_here'")
    st.stop()

genai.configure(api_key=API_KEY)

def get_current_utc_time():
    """
    Returns the current time in UTC timezone.
    """
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

def get_current_local_time(timezone_name="Asia/Kolkata"): # Defaulting to user's location (Mumbai)
    """
    Returns the current local time for a given timezone.
    Defaults to Asia/Kolkata (Mumbai) if no timezone is specified.
    """
    try:
        tz = pytz.timezone(timezone_name)
        local_time = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z%z")
        return local_time
    except pytz.UnknownTimeZoneError:
        return f"Error: Unknown timezone '{timezone_name}'. Please provide a valid timezone name (e.g., 'America/New_York')."

def initialize_chat_session():
    """Initializes a new Gemini chat session with defined tools and persona."""
    available_tools = [
        {
            "function_declarations": [
                {
                    "name": "get_current_utc_time",
                    "description": "Returns the current time in UTC timezone. Use this when the user asks for the current UTC time, date, or 'what time is it in UTC'.",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {},
                    },
                },
                {
                    "name": "get_current_local_time",
                    "description": "Returns the current local time for a specified timezone. Defaults to Asia/Kolkata if no timezone is provided. Use this when the user asks for local time, or general time/date without specifying UTC, or wants a greeting based on time of day.",
                    "parameters": {
                        "type": "OBJECT",
                        "properties": {
                            "timezone_name": {
                                "type": "STRING",
                                "description": "The name of the timezone (e.g., 'America/New_York', 'Europe/London', 'Asia/Kolkata'). Defaults to 'Asia/Kolkata'."
                            }
                        },
                        "required": []
                    },
                }
            ]
        }
    ]

    model = genai.GenerativeModel('gemini-1.5-flash', tools=available_tools)
    
    chat_session = model.start_chat(history=[
        {
            "role": "user",
            "parts": [
                "You are a helpful and knowledgeable assistant. You can tell me the current UTC time or local time anywhere in the world if asked. When greeting the user, try to use the current local time to say good morning/afternoon/evening. Make your responses concise and friendly."
            ]
        },
        {
            "role": "model",
            "parts": [
                "Hello! I'm ready to help you with your questions. How can I assist you today?"
            ]
        }
    ])
    return chat_session

st.set_page_config(page_title="Chatbot", layout="centered")
st.title("Chatbot")

with st.sidebar:
    st.header("Chat Controls")
    if st.button("Clear Chat / Start New Conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.chat_session = initialize_chat_session()
        st.session_state.messages.append({"role": "model", "parts": st.session_state.chat_session.history[1].parts[0].text})
        st.rerun() 

if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    st.session_state.chat_session = initialize_chat_session()
    st.session_state.messages.append({"role": "model", "parts": st.session_state.chat_session.history[1].parts[0].text})


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["parts"])


if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "parts": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    if prompt.lower().strip() in ["exit", "quit"]:
        farewells = ["Goodbye! It was nice chatting with you. To start a new conversation, click 'Clear Chat' in the sidebar.",
                     "See you next time! Feel free to reach out anytime. Use the 'Clear Chat' button to begin fresh.",
                     "Farewell! Hope you have a great day. If you want to chat again, just clear the chat!"]
        bot_farewell = random.choice(farewells)
        st.session_state.messages.append({"role": "model", "parts": bot_farewell})
        with st.chat_message("model"):
            st.markdown(bot_farewell)
        st.stop() 
        

    with st.chat_message("model"):
        response_container = st.empty()
        thinking_dots = ""
        
        for i in range(1, 4):
            thinking_dots = "." * i
            response_container.markdown(f"Bot is thinking{thinking_dots}")
            time.sleep(0.3)
        
        try:
            response = st.session_state.chat_session.send_message(prompt, stream=True)

            full_response_text = ""
            for chunk in response:
                if chunk.parts:
                    tool_called = False
                    for part in chunk.parts:
                        if part.function_call:
                            tool_called = True
                            function_name = part.function_call.name
                            function_args = {k: v for k, v in part.function_call.args.items()}

                            st.info(f"Bot is performing an action: Calling '{function_name}'...")

                            result = ""
                            if function_name == "get_current_utc_time":
                                result = get_current_utc_time()
                            elif function_name == "get_current_local_time":
                                result = get_current_local_time(**function_args)
                            else:
                                result = f"Error: Unknown function '{function_name}' requested."

                            st.success(f"Function '{function_name}' returned: {result}")

                            st.session_state.chat_session.send_message(
                                genai.protos.Part(
                                    function_response=genai.protos.FunctionResponse(
                                        name=function_name,
                                        response={"content": result}
                                    )
                                )
                            )
                            break 

                    if not tool_called:
                        for part in chunk.parts:
                            if part.text:
                                full_response_text += part.text
                                response_container.markdown(full_response_text + "▌") 
            
            response_container.markdown(full_response_text)
            
            st.session_state.messages.append({"role": "model", "parts": full_response_text})

        except Exception as e:
            st.error(f"Error: Could not get a response from the bot. Details: {e}")
            st.session_state.messages.append({"role": "model", "parts": f"Sorry, something went wrong: {e}"})
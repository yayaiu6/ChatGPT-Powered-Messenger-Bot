import logging
import os
import openai
import requests
import sqlite3
from flask import Flask, request
from env import *

# Set up logging to track events and errors
logging.basicConfig(level=logging.INFO)

# Load API keys and tokens from environment variables in env.py
openai.api_key = os.getenv('OPENAI_API_KEY')
FB_ACCESS_TOKEN = os.getenv('FB_ACCESS_TOKEN')
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

# Initialize Flask application
app = Flask(__name__)

# Function to set up the SQLite database
def init_db():
    # Connect to the SQLite database file 'chat_history.db'
    conn = sqlite3.connect('chat_history.db')
    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()
    # Create a table 'chat_history' if it doesn't exist, with columns for user ID, message, and response
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            user_id TEXT,
            user_message TEXT,
            assistant_response TEXT
        )
    ''')
    # Commit the changes to the database
    conn.commit()
    # Close the database connection
    conn.close()

# Call the database initialization function when the app starts
init_db()

# Function to generate a response using OpenAI's GPT-3.5-turbo
def generate_openai_response(user_message, chat_history):
    try:
        # Define the system message to set the assistant's role and behavior
        messages = [
            {
                "role": "system",
                "content": """
                You are a smart assistant working for ESHRAQ AI, a company specializing in AI solutions for businesses.
                Your task is to respond to clients and convince them to integrate AI systems (like smart chatbots) into their companies
                to improve performance and efficiency. Use simple, clear language and provide practical examples or solutions when needed.
                """
            }
        ]

        # Add the last 5 messages from chat history to maintain context
        for entry in chat_history[-5:]:  # Limit to the last 5 entries
            messages.append({"role": "user", "content": entry[0]})  # User's previous message
            messages.append({"role": "assistant", "content": entry[1]})  # Assistant's previous response

        # Add the current user message to the list
        messages.append({"role": "user", "content": user_message})

        # Call OpenAI API to generate a response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        # Check if the response contains valid choices and return the first one
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['message']['content']
        else:
            return "Sorry, I couldn’t generate a response."
    except Exception as e:
        # Log any errors that occur during response generation
        logging.error(f"Error generating response: {e}")
        return "An error occurred, please try again later."

# Function to save a message and response to the database
def save_message_to_db(user_id, message, response):
    # Connect to the database
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    # Insert the user ID, message, and response into the chat_history table
    cursor.execute('INSERT INTO chat_history (user_id, user_message, assistant_response) VALUES (?, ?, ?)',
                   (user_id, message, response))
    # Commit the changes
    conn.commit()
    # Close the connection
    conn.close()

# Function to retrieve chat history for a specific user
def get_chat_history(user_id):
    # Connect to the database
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    # Select all previous messages and responses for the given user_id
    cursor.execute('SELECT user_message, assistant_response FROM chat_history WHERE user_id = ?', (user_id,))
    # Fetch all results as a list of tuples
    chat_history = cursor.fetchall()
    # Close the connection
    conn.close()
    # Return the chat history
    return chat_history

# Function to send a message back to the user via Facebook Messenger
def send_message(sender_id, message_text):
    # Construct the Facebook Graph API URL with the access token
    url = f'https://graph.facebook.com/v12.0/me/messages?access_token={FB_ACCESS_TOKEN}'
    # Define the payload for the API request
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": sender_id},
        "message": {"text": message_text}
    }
    # Send the POST request to the Facebook API
    response = requests.post(url, json=payload)
    # Log an error if the request fails
    if response.status_code != 200:
        logging.error(f"Error sending message: {response.status_code} {response.text}")

# Webhook endpoint to handle incoming requests from Facebook
@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Handle GET requests for webhook verification
    if request.method == "GET":
        # Get the verification token and challenge from the request
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        # Verify the token matches the expected value
        if verify_token == VERIFY_TOKEN:
            return challenge, 200  # Return the challenge to confirm verification
        else:
            return "Verification token mismatch", 403  # Return an error if verification fails

    # Handle POST requests for incoming messages
    elif request.method == "POST":
        # Parse the incoming JSON data from Facebook
        data = request.get_json()
        logging.info(f"Received data: {data}")
        
        # Check if the data is related to a page (Messenger event)
        if data.get("object") == "page":
            # Loop through each entry in the data
            for entry in data.get("entry", []):
                # Loop through each messaging event in the entry
                for messaging_event in entry.get("messaging", []):
                    # Extract the sender's ID
                    sender_id = messaging_event["sender"].get("id")

                    # Check if the event contains a message
                    if "message" in messaging_event:
                        # Get the text of the user's message
                        message_text = messaging_event["message"].get("text", "")
                        logging.info(f"Received message from {sender_id}: {message_text}")

                        # Retrieve the user's chat history
                        chat_history = get_chat_history(sender_id)
                        # Generate a response using OpenAI
                        response_text = generate_openai_response(message_text, chat_history)

                        # If a response is generated, send it and save it
                        if response_text:
                            send_message(sender_id, response_text)
                            save_message_to_db(sender_id, message_text, response_text)
                        else:
                            logging.warning(f"No response generated for message from {sender_id}")

            return "ok"  # Return success status

        return "Invalid object", 400  # Return error if the object is not a page

# Root endpoint to confirm the webhook is active
@app.route('/')
def home():
    return "Webhook is active and running!"

# Test endpoint to verify the app is running
@app.route('/test')
def hello():
    return "Hello, World!"

# Run the Flask app if this file is executed directly
if __name__ == '__main__':
    app.run(port=5001, debug=True)
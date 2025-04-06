# ChatGPT-Powered Messenger Bot

This is an old project I worked on back in 2024 during my exploration of AI-powered solutions. I decided to share it here on GitHub to benefit others who might find it useful as a starting point for building their own chatbots or learning about integrating AI with messaging platforms. It’s a simple yet functional chatbot built with Flask, integrated with Facebook Messenger, and powered by OpenAI’s GPT-3.5-turbo model. I hope you find it helpful—feel free to use it, improve it, or adapt it for your own needs!

---

### What Does This Code Do?
This project is a chatbot designed to interact with users on Facebook Messenger. It leverages OpenAI’s GPT-3.5-turbo model to generate smart responses and stores conversation history in a SQLite database to maintain context. The bot’s primary goal is to convince businesses to adopt AI solutions (like chatbots) to enhance their performance and efficiency, as if it’s a promotional tool for a fictional company called "ESHRAQ AI."

#### Benefits
- **Context-Aware Responses**: Remembers up to the last 5 messages to provide coherent replies.
- **Business Promotion**: Demonstrates how AI can improve customer service and efficiency.
- **Learning Tool**: Great for understanding Flask, OpenAI integration, and Facebook Messenger API usage.
- **Customizable**: Easy to tweak for different purposes or platforms.

---

### Code Explanation
Here’s a breakdown of the main components of the code:

1. **`init_db()`**
   - Initializes a SQLite database (`chat_history.db`) with a table called `chat_history` to store user IDs, their messages, and the bot’s responses.

2. **`generate_openai_response(user_message, chat_history)`**
   - Uses OpenAI’s GPT-3.5-turbo to generate responses based on the user’s message and the last 5 entries of chat history. It’s configured to act as an ESHRAQ AI assistant promoting AI solutions.

3. **`save_message_to_db(user_id, message, response)`**
   - Saves each conversation (user message and bot response) to the SQLite database for future reference.

4. **`get_chat_history(user_id)`**
   - Retrieves the chat history for a specific user from the database, enabling context-aware responses.

5. **`send_message(sender_id, message_text)`**
   - Sends the bot’s response back to the user via the Facebook Messenger API.

6. **`webhook()`**
   - The core endpoint that handles:
     - **GET requests**: Verifies the webhook with Facebook.
     - **POST requests**: Processes incoming messages, generates responses, and sends them back.

7. **`home()` and `hello()`**
   - Simple endpoints (`/` and `/test`) to confirm the app is running.

---

### How to Use It
Follow these steps to set up and run the chatbot on your own machine:

#### Prerequisites
- Python 3.x installed.
- A Facebook Developer account and a Facebook Page with Messenger enabled (note: this works with Pages, not personal accounts).
- An OpenAI API key.

#### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/chatgpt-messenger-bot.git
   cd chatgpt-messenger-bot


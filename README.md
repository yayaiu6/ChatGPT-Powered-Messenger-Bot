# Connecting ChatGPT to a Facebook Messenger Account

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
- A Facebook Developer account and a Facebook app with Messenger enabled.
- An OpenAI API key.

#### Setup Instructions
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/eshraq-ai-chatbot.git
   cd eshraq-ai-chatbot
   ```

2. **Install Dependencies**
   Install the required Python libraries:
   ```bash
   pip install -r requirements.txt
   ```
   The `requirements.txt` includes:
   ```
   flask
   openai
   requests
   sqlite3
   ```

3. **Set Up Environment Variables**
   - Create a file named `env.py` in the project root.
   - Add the following variables (replace with your own keys):
     ```python
     import os
     os.environ['OPENAI_API_KEY'] = 'your-openai-api-key'
     os.environ['FB_ACCESS_TOKEN'] = 'your-facebook-access-token'
     os.environ['VERIFY_TOKEN'] = 'your-custom-verify-token'
     ```

4. **Run the Application**
   Start the Flask server:
   ```bash
   python app.py
   ```
   The app will run on `http://localhost:5001`.

5. **Expose Your Local Server**
   - Use a tool like [ngrok](https://ngrok.com/) to make your local server accessible online:
     ```bash
     ngrok http 5001
     ```
   - Copy the public URL (e.g., `https://your-ngrok-url.ngrok.io`).

6. **Configure Facebook Webhook**
   - Go to your Facebook Developer account.
   - In your app’s Messenger settings, set the webhook URL to `https://your-ngrok-url.ngrok.io/webhook`.
   - Use the `VERIFY_TOKEN` you defined in `env.py` for verification.
   - Subscribe to the "messages" event.

7. **Test the Chatbot**
   - Send a message to your Facebook page via Messenger, and the bot should respond!

---

### Tips for Users
- **Test Locally First**: Use the `/test` endpoint (`http://localhost:5001/test`) to ensure the app runs correctly.
- **Secure Your Keys**: Never commit `env.py` to GitHub—keep it in `.gitignore`.
- **Customize the Bot**: Edit the system prompt in `generate_openai_response` to change the bot’s personality or purpose.
- **Scale It**: Add more features like message classification or support for other platforms (e.g., WhatsApp).
- **Debugging**: Check the console logs (thanks to `logging`) if something goes wrong.

---

### Notes
- This was a proof-of-concept project from 2024, so it’s not production-ready but works well as a foundation.
- Contributions are welcome—feel free to submit pull requests or suggestions!



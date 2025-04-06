
# ChatGPT-Powered Messenger Bot

This project creates a chatbot that talks to users on Facebook Messenger. It uses OpenAI’s GPT-3.5-turbo to generate clever, context-aware responses and saves chat history in a SQLite database so it can “remember” conversations. The bot is designed to promote AI solutions to businesses, but you can tweak it for any purpose you like!

### Why Use This Bot?
- **Smarter Conversations**: It keeps track of the last 5 messages to give better replies.
- **Business-Friendly**: Shows how AI can save time and improve customer service.
- **Learning Tool**: Perfect for understanding Flask, OpenAI, and Facebook Messenger integration.
- **Flexible**: Change it up to suit your needs—add features or connect it to other platforms!

---

## How It Works: Code Breakdown

Here’s a closer look at what’s inside the code:

1. **`init_db()`**  
   - Creates a SQLite database called `chat_history.db`.  
   - Sets up a table to store user IDs, their messages, and the bot’s replies.

2. **`generate_openai_response(user_message, chat_history)`**  
   - Takes the user’s message and their recent chat history.  
   - Sends them to OpenAI’s GPT-3.5-turbo to get a smart response.  
   - You can tweak the “system prompt” here to make the bot funny, formal, or whatever vibe you want!

3. **`save_message_to_db(user_id, message, response)`**  
   - Saves the user’s message and the bot’s reply in the database.  
   - Keeps everything organized by user ID.

4. **`get_chat_history(user_id)`**  
   - Grabs the last 5 messages for a user from the database.  
   - Helps the bot remember what’s been said so it doesn’t sound clueless.

5. **`send_message(sender_id, message_text)`**  
   - Uses Facebook’s API to send the bot’s response back to the user on Messenger.  
   - Needs a Facebook access token to work (more on that later).

6. **`webhook()`**  
   - The “listener” for your bot.  
   - Handles two things:  
     - **Verification**: Confirms your app with Facebook when you set it up.  
     - **Messages**: Processes incoming messages from users and triggers replies.

7. **`home()` and `hello()`**  
   - Simple pages (like `/` and `/test`) to check if your Flask app is running.

---

## Key Integrations: ngrok, Facebook, and OpenAI

This bot connects three big tools: ngrok, Facebook Messenger, and OpenAI. Let’s dive into each one so you know exactly what’s happening.

### ngrok: Making Your Local Server Public
- **What is it?**  
  ngrok is a free tool that takes your local server (running on your computer) and gives it a public web address. Think of it like a bridge between your machine and the internet.

- **Why do we need it?**  
  Your Flask app runs on `http://localhost:5001`—great for testing, but Facebook Messenger can’t reach it because it’s not online. ngrok fixes this by creating a temporary public URL (like `https://abc123.ngrok.io`) that Facebook can talk to.

- **How does it work?**  
  - You run ngrok on your computer alongside your Flask app.  
  - It “tunnels” traffic from the public URL to your local server.  
  - Every time you start ngrok, you get a new URL, so you’ll update Facebook with it each time.

- **Extra Tips**:  
  - ngrok is free for basic use, but the free URLs expire after a few hours.  
  - For a permanent solution, you’d host your app on a real server (like Heroku or AWS) instead.

### Facebook Messenger: Connecting to Users
- **What’s the deal?**  
  This bot lives on Facebook Messenger, tied to a Facebook Page (not your personal profile). You’ll need a Facebook Developer account to set it up.

- **Key Pieces**:  
  - **Facebook Page**: The bot “belongs” to a Page you own (e.g., “My Cool Business”).  
  - **Facebook App**: You’ll create an app in the Facebook Developer portal to connect your code to Messenger.  
  - **Page Access Token**: A secret key that lets your bot send messages as your Page.  
  - **Webhook**: A URL where Facebook sends user messages for your bot to process.

- **How it fits in**:  
  - When someone messages your Page, Facebook sends the message to your ngrok URL (e.g., `https://abc123.ngrok.io/webhook`).  
  - Your Flask app grabs the message, processes it with OpenAI, and sends a reply back through Facebook’s API.

- **Why Messenger?**  
  It’s popular, easy to set up, and lets you reach users where they already hang out.

### OpenAI: Powering the Brain
- **What is it?**  
  OpenAI is the company behind ChatGPT. We’re using their GPT-3.5-turbo model, which is fast, smart, and great for conversations.

- **How does it work here?**  
  - You get an API key from OpenAI (like a password to use their service).  
  - The bot sends the user’s message and chat history to OpenAI via their API.  
  - OpenAI sends back a response, which the bot passes to the user.

- **Why GPT-3.5-turbo?**  
  - It’s powerful but cheaper and faster than newer models like GPT-4.  
  - Perfect for a demo like this—smart enough to impress without breaking the bank.

- **Cool Detail**:  
  You can tweak how the bot talks by changing the “system prompt” (e.g., “Act like a friendly teacher” or “Be a sassy robot”). It’s all in the `generate_openai_response` function.

---

## How to Set It Up

Ready to get this bot running? Follow these steps carefully—I’ve made them super clear so you won’t get lost.

### What You’ll Need
- **Python 3.x**: Make sure it’s installed (check with `python --version`).  
- **Facebook Developer Account**: Sign up at [developers.facebook.com](https://developers.facebook.com/).  
- **Facebook Page**: Create one if you don’t have it (e.g., “My Bot Page”).  
- **OpenAI API Key**: Get one from [platform.openai.com](https://platform.openai.com/).  
- **ngrok**: Download it from [ngrok.com](https://ngrok.com/).

### Step-by-Step Instructions

1. **Clone the Repository**  
   Grab the code from GitHub:  
   ```bash
   git clone https://github.com/your-username/chatgpt-messenger-bot.git
   cd chatgpt-messenger-bot
   ```
   *(Replace `your-username` with your GitHub username.)*

2. **Install the Libraries**  
   You’ll need a few Python libraries. Install them with these commands:  
   ```bash
   pip install flask openai requests
   ```
   - **flask**: Runs the web server.  
   - **openai**: Talks to OpenAI’s API.  
   - **requests**: Sends messages to Facebook.  
   - *(Good news: `sqlite3` and `logging` come with Python, so no extra downloads!)*

3. **Set Up Your Secrets**  
   - Create a file called `env.py` in the project folder.  
   - Add these lines with your own keys:  
     ```python
     import os
     os.environ['OPENAI_API_KEY'] = 'your-openai-api-key-here'
     os.environ['FB_ACCESS_TOKEN'] = 'your-facebook-page-access-token'
     os.environ['VERIFY_TOKEN'] = 'any-random-string-you-choose'
     ```
   - **Where to get them**:  
     - OpenAI key: From OpenAI’s website.  
     - Facebook token: From your Facebook app setup (Step 6).  
     - Verify token: Make up a random word or phrase (e.g., “mysecret”).  
   - **Security Tip**: Add `env.py` to `.gitignore` so it doesn’t go public!

4. **Run the Bot**  
   Start the Flask app:  
   ```bash
   python app.py
   ```
   - It’ll run on `http://localhost:5001`. Open that in your browser to see “Hello, World!” and confirm it’s working.

5. **Expose It with ngrok**  
   - Open a new terminal (keep the app running).  
   - Run ngrok to connect port 5001 to the internet:  
     ```bash
     ngrok http 5001
     ```
   - Look for a line like `Forwarding https://abc123.ngrok.io -> http://localhost:5001`.  
   - Copy that `https://abc123.ngrok.io` URL—you’ll need it next.

6. **Set Up Facebook Messenger**  
   - Go to [developers.facebook.com](https://developers.facebook.com/).  
   - Click “My Apps” > “Create App”.  
   - Choose “Other” > “Business” > Give it a name (e.g., “My Chatbot”).  
   - In the app dashboard:  
     - Add the “Messenger” product.  
     - Under “Messenger Settings”:  
       - Link your Facebook Page.  
       - Generate a **Page Access Token** (copy it to `env.py`).  
       - Scroll to “Webhooks” > “Edit Subscription”.  
         - Set the Callback URL to `https://abc123.ngrok.io/webhook` (your ngrok URL + `/webhook`).  
         - Set the Verify Token to whatever you put in `env.py` (e.g., “mysecret”).  
         - Click “Verify and Save”.  
       - Subscribe to “messages” so your bot gets user messages.

7. **Test It Out!**  
   - Open Messenger on your phone or computer.  
   - Message your Facebook Page (e.g., “Hi, how’s it going?”).  
   - The bot should reply with a ChatGPT-powered response!  
   - Check your `chat_history.db` file—it’ll grow as you chat.

---

## Tips to Make It Yours

- **Check It’s Working**: Visit `http://localhost:5001/test` to see a test page.  
- **Keep Secrets Safe**: Never share `env.py`—it’s your key to the kingdom!  
- **Change the Bot’s Vibe**: Edit the system prompt in `generate_openai_response` (e.g., “You’re a pirate” for “Argh, matey!” replies).  
- **Add Cool Stuff**: Try classifying messages (happy/sad) or connecting to WhatsApp.  
- **Fix Problems**: Watch the terminal for error messages if something goes wrong.


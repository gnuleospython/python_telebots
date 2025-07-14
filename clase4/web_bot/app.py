from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from dotenv import load_dotenv
import google.generativeai as ai

load_dotenv()
API_KEY = os.getenv("API_KEY_GEMINI")
ai.configure(api_key=API_KEY)

preferred_models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest", 
    "gemini-2.5-flash-002",   
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-002",
]

model_to_use = None
for m in ai.list_models():
    if "generateContent" in m.supported_generation_methods:
        for preferred in preferred_models:
            if m.name == f"models/{preferred}":
                model_to_use = m.name
                break
    if model_to_use:
        break

if not model_to_use:
    raise Exception("No Gemini model available for generateContent")

model = ai.GenerativeModel(model_to_use)
chat = model.start_chat()

# --- Flask Setup ---
app = Flask(__name__)
DATABASE = 'chat.db'

# --- Database Helper Functions ---
def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT NOT NULL,
            bot_response TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("SELECT user_message, bot_response, timestamp FROM messages ORDER BY id ASC")
    chat_history = c.fetchall()
    conn.close()
    return render_template('index.html', chat_history=chat_history)

@app.route('/send', methods=['POST'])
def send():
    user_message = request.form['message']
    try:
        response = chat.send_message(user_message)
        bot_response = response.text
    except Exception as e:
        bot_response = f"Error: {e}"

    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user_message, bot_response) VALUES (?, ?)", (user_message, bot_response))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/clear')
def clear():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM messages")
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

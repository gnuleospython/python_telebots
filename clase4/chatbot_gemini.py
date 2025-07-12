import google.generativeai as ai
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY_GEMINI")

ai.configure(api_key=API_KEY)

print("Checking available models for generateContent:")
model_to_use = None

preferred_models = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest", 
    "gemini-2.5-flash-002",   
    "gemini-2.5-pro",
    "gemini-2.5-pro-latest",  
    "gemini-2.5-pro-002",   
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-002",
]

available_models = []
for m in ai.list_models():
    if "generateContent" in m.supported_generation_methods:
        full_model_name = m.name
        available_models.append(full_model_name)
        print(f"- {full_model_name}") 

for preferred in preferred_models:
    if f"models/{preferred}" in available_models:
        model_to_use = f"models/{preferred}"
        break

if not model_to_use:
    print("\nError: No suitable 'gemini' model found that supports 'generateContent' from the preferred list.")
    print("Please review the available models printed above and manually update 'preferred_models' in the script.")
    exit() 
else:
    print(f"\nUsing model: {model_to_use}")
    model = ai.GenerativeModel(model_to_use)

chat = model.start_chat()

while True:
    message = input('You: ')
    if message.lower() == 'bye':
        print('Chatbot: Goodbye!')
        break
    try:
        response = chat.send_message(message)
        print('Chatbot:', response.text)
    except Exception as e:
        print(f"An error occurred while sending message: {e}")
        print("Please try again or restart the chat.")
        

import sqlite3
import os
import re
import requests
import telebot
from telebot import types
from datetime import datetime
from dotenv import load_dotenv

# Obtine el token del bot de las variables de entorno
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: La variable de entorno TELEGRAM_BOT_TOKEN no está configurada.")
    print("Por favor, asegúrate de establecerla antes de ejecutar el script.")
    exit() # Salir del script si no hay token

# Inicializa el bot
bot = telebot.TeleBot(BOT_TOKEN)

# Responde al comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):

    user_name = message.from_user.first_name if message.from_user.first_name else "usuario"
    bot.reply_to(message, f"¡Hola, {user_name}!\n Somos Terra Habitat Bienes Raices\n Selecciona una opción para poderte ayudar")
    #print(f"Comando /start recibido de {message.from_user.username}")


# Inicializa el bot para que empiece a escuchar mensajes
print("Bot iniciando... Presiona Ctrl+C para detenerlo.")
bot.polling(none_stop=True, interval=0) # none_stop=True para que siga funcionando, interval=0 para polling rápido















# # 4. Manejador para el comando /help
# @bot.message_handler(commands=['help'])
# def send_help(message):
#     """
#     Responde al comando /help.
#     """
#     help_text = """
#     Estos son los comandos que entiendo:
#     /start - Inicia el bot y saluda.
#     /help - Muestra este mensaje de ayuda.
#     /echo [texto] - Repite el texto que le envíes.
#     También puedo responder a cualquier mensaje de texto.
#     """
#     bot.reply_to(message, help_text)
#     print(f"Comando /help recibido de {message.from_user.username}")

# # 5. Manejador para el comando /echo (con parámetros)
# @bot.message_handler(commands=['echo'])
# def echo_all(message):
#     """
#     Repite el texto que sigue al comando /echo.
#     """
#     if len(message.text.split()) > 1:
#         text_to_echo = " ".join(message.text.split()[1:])
#         bot.reply_to(message, f"Me pediste que repita: {text_to_echo}")
#     else:
#         bot.reply_to(message, "Por favor, usa el comando /echo seguido del texto que quieres que repita. Ejemplo: /echo Hola mundo")
#     print(f"Comando /echo recibido de {message.from_user.username}")

# # 6. Manejador para mensajes de texto genéricos (cualquier otro mensaje que no sea un comando)
# @bot.message_handler(func=lambda message: True) # La función lambda 'True' hace que maneje todos los mensajes
# def echo_message(message):
#     """
#     Responde a cualquier mensaje de texto que no sea un comando.
#     """
#     bot.reply_to(message, f"Recibí tu mensaje: '{message.text}'")
#     print(f"Mensaje de texto recibido de {message.from_user.username}: '{message.text}'")

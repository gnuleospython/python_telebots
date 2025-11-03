from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters, ConversationHandler
)
from mailjet_rest import Client
import requests
import os
import re
import sqlite3
from datetime import datetime
from dotenv import load_dotenv
from telebot import TeleBot, types
import datetime

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# Estado temporal de los usuarios
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Hola...\nTe saluda Terra Habitat Bienes Raices\nPor favor, escribe tu nombre completo:")
    bot.register_next_step_handler(message, process_nombre)

def process_nombre(message):
    user_data[message.chat.id] = {"nombre": message.text}
    
    bot.send_message(message.chat.id, "¿Qué servicio deseas? \n (Compra - Venta - Alquiler - Avalúo - Administración - Otro Servicio)")
    bot.register_next_step_handler(message, process_servicio)

def process_servicio(message):
    user_data[message.chat.id]["servicio"] = message.text
    
    bot.send_message(message.chat.id, "Ayudame con tu número de teléfono")
    bot.register_next_step_handler(message, process_telefono)

def process_telefono(message):
    user_data[message.chat.id]["telefono"] = message.text
    
    bot.send_message(message.chat.id, "Ayudame con tu correo electrónico")
    bot.register_next_step_handler(message, cita)
    
def cita(message):
    user_data[message.chat.id]["time"] = message.text
    data = user_data[message.chat.id]
    
    bot.send_message(message.chat.id, "🔹¡Tu cita ha sido registrada!\nUn Asesor te atendera de forma presonalizada")
    resumen = f"🗓️*Resumen de tu cita:*\nNombre: {data['nombre']}\nServicio: {data['servicio']}\nTelefono: {data['telefono']}"
    
    bot.send_message(message.chat.id, resumen, parse_mode='Markdown')


if __name__ == "__main__":
    print("Bot ejecutándose...")
    bot.infinity_polling()
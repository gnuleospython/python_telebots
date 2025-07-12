# telebot_app.py

from telebot import TeleBot, types
from dotenv import load_dotenv
import datetime

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = TeleBot(BOT_TOKEN)

# Estado temporal de los usuarios
user_data = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 ¡Bienvenido al sistema de agendamiento de citas del SPA!\nPor favor, escribe tu nombre completo:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    user_data[message.chat.id] = {"name": message.text}
    bot.send_message(message.chat.id, "¿Qué servicio deseas agendar? (Ej: masaje, facial, depilación)")
    bot.register_next_step_handler(message, process_service)

def process_service(message):
    user_data[message.chat.id]["service"] = message.text
    bot.send_message(message.chat.id, "¿Qué fecha deseas? (Formato: YYYY-MM-DD)")
    bot.register_next_step_handler(message, process_date)

def process_date(message):
    try:
        fecha = datetime.datetime.strptime(message.text, '%Y-%m-%d').date()
        user_data[message.chat.id]["date"] = str(fecha)
        bot.send_message(message.chat.id, "¿A qué hora? (Ej: 15:30)")
        bot.register_next_step_handler(message, process_time)
    except ValueError:
        bot.send_message(message.chat.id, "Formato de fecha inválido. Intenta nuevamente (YYYY-MM-DD)")
        bot.register_next_step_handler(message, process_date)

def process_time(message):
    user_data[message.chat.id]["time"] = message.text
    data = user_data[message.chat.id]
    resumen = f"📝 *Resumen de tu cita:*\nNombre: {data['name']}\nServicio: {data['service']}\nFecha: {data['date']}\nHora: {data['time']}"
    bot.send_message(message.chat.id, resumen, parse_mode='Markdown')
    bot.send_message(message.chat.id, "✅ ¡Tu cita ha sido registrada! Gracias por confiar en nuestro SPA ✨")

if __name__ == "__main__":
    print("Bot ejecutándose...")
    bot.infinity_polling()
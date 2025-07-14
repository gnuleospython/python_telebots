import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
import sqlite3
import json
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Inicializar bot
bot = telebot.TeleBot(BOT_TOKEN)

# Base de datos

def init_db():
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            nombre TEXT,
            telefono TEXT,
            email TEXT,
            direccion TEXT,
            productos TEXT,
            total REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def guardar_pedido(user_id, datos):
    conn = sqlite3.connect("chat.db")
    c = conn.cursor()
    c.execute('''
        INSERT INTO pedidos (user_id, nombre, telefono, email, direccion, productos, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        datos["nombre"],
        datos["telefono"],
        datos["email"],
        datos["direccion"],
        json.dumps(datos["productos"]),
        datos["total"]
    ))
    conn.commit()
    conn.close()

# Datos temporales por usuario
usuarios = {}

# Estados
ESTADOS = {
    "MENU": "menu",
    "PEDIDO_NOMBRE": "nombre",
    "PEDIDO_TELEFONO": "telefono",
    "PEDIDO_EMAIL": "email",
    "PEDIDO_DIRECCION": "direccion"
}

# Productos
PRODUCTOS = {
    "1": {"nombre": "Vino de Uva Premium", "precio": 25.00},
    "2": {"nombre": "Vino de Morti\u00f1o", "precio": 30.00},
    "3": {"nombre": "Vino de Ar\u00e1ndano", "precio": 28.00},
    "4": {"nombre": "Chocolate Cl\u00e1sico", "precio": 8.00},
    "5": {"nombre": "Chocolate Premium", "precio": 12.00},
    "6": {"nombre": "Chocolate Especial", "precio": 15.00}
}

# Saludo inicial
@bot.message_handler(commands=["start"])
def start(message: Message):
    user_id = message.from_user.id
    usuarios[user_id] = {"estado": ESTADOS["MENU"], "carrito": []}

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1. Ver Cat\u00e1logo de Vinos", "2. Ver Cat\u00e1logo de Chocolates", "0. Salir")

    texto = """
👋 *\u00a1Hola! Bienvenido a La R\u00fastica* 🍷🍫

1. Ver Cat\u00e1logo de Vinos
2. Ver Cat\u00e1logo de Chocolates
0. Salir

Elige una opci\u00f3n:
    """
    bot.send_message(user_id, texto, reply_markup=markup, parse_mode="Markdown")

# Mostrar cat\u00e1logo

def mostrar_catalogo_vinos(user_id):
    texto = "🍷 *Cat\u00e1logo de Vinos*\n"
    texto += "1. Vino de Uva Premium - $25.00\n"
    texto += "2. Vino de Morti\u00f1o - $30.00\n"
    texto += "3. Vino de Ar\u00e1ndano - $28.00\n"
    texto += "\nEscribe el n\u00famero del producto para seleccionarlo, o 0 para salir."
    bot.send_message(user_id, texto, parse_mode="Markdown")

def mostrar_catalogo_chocolates(user_id):
    texto = "🍫 *Chocolates La R\u00fastica*\n"
    texto += "4. Chocolate Cl\u00e1sico - $8.00\n"
    texto += "5. Chocolate Premium - $12.00\n"
    texto += "6. Chocolate Especial - $15.00\n"
    texto += "\nEscribe el n\u00famero del producto para seleccionarlo, o 0 para salir."
    bot.send_message(user_id, texto, parse_mode="Markdown")

# Agregar producto y pedir datos

def agregar_y_pedir(user_id, codigo):
    producto = PRODUCTOS.get(codigo)
    if producto:
        usuarios[user_id]["carrito"].append(producto)
        total = sum(p["precio"] for p in usuarios[user_id]["carrito"])
        usuarios[user_id]["pedido"] = {
            "productos": usuarios[user_id]["carrito"],
            "total": total
        }
        usuarios[user_id]["estado"] = ESTADOS["PEDIDO_NOMBRE"]
        bot.send_message(user_id, f"🛒 {producto['nombre']} a\u00f1adido al carrito.")
        bot.send_message(user_id, "👤 Ingresa tu nombre completo o escribe 0 para salir:")
    else:
        bot.send_message(user_id, "Producto no v\u00e1lido.")

# Manejador de mensajes

@bot.message_handler(func=lambda m: True)
def handle_message(message: Message):
    user_id = message.from_user.id
    texto = message.text.strip()

    if user_id not in usuarios:
        usuarios[user_id] = {"estado": ESTADOS["MENU"], "carrito": []}

    if texto == "0":
        usuarios[user_id] = {"estado": ESTADOS["MENU"], "carrito": []}
        bot.send_message(user_id, "❌ Proceso cancelado.")
        return start(message)

    estado = usuarios[user_id]["estado"]

    if estado == ESTADOS["MENU"]:
        if texto == "1. Ver Cat\u00e1logo de Vinos":
            mostrar_catalogo_vinos(user_id)
        elif texto == "2. Ver Cat\u00e1logo de Chocolates":
            mostrar_catalogo_chocolates(user_id)
        elif texto in PRODUCTOS:
            agregar_y_pedir(user_id, texto)
        else:
            bot.send_message(user_id, "Por favor, selecciona una opci\u00f3n del men\u00fa.")

    elif estado == ESTADOS["PEDIDO_NOMBRE"]:
        usuarios[user_id]["pedido"]["nombre"] = texto
        usuarios[user_id]["estado"] = ESTADOS["PEDIDO_TELEFONO"]
        bot.send_message(user_id, "📞 Ingresa tu tel\u00e9fono o escribe 0 para salir:")

    elif estado == ESTADOS["PEDIDO_TELEFONO"]:
        usuarios[user_id]["pedido"]["telefono"] = texto
        usuarios[user_id]["estado"] = ESTADOS["PEDIDO_EMAIL"]
        bot.send_message(user_id, "📧 Ingresa tu email o escribe 0 para salir:")

    elif estado == ESTADOS["PEDIDO_EMAIL"]:
        usuarios[user_id]["pedido"]["email"] = texto
        usuarios[user_id]["estado"] = ESTADOS["PEDIDO_DIRECCION"]
        bot.send_message(user_id, "📍 Ingresa tu direcci\u00f3n o escribe 0 para salir:")

    elif estado == ESTADOS["PEDIDO_DIRECCION"]:
        usuarios[user_id]["pedido"]["direccion"] = texto
        guardar_pedido(user_id, usuarios[user_id]["pedido"])
        bot.send_message(user_id, "✅ Pedido guardado correctamente. Te contactaremos pronto. 🎉")
        usuarios[user_id] = {"estado": ESTADOS["MENU"], "carrito": []}
        start(message)
    else:
        bot.send_message(user_id, "Usa el men\u00fa para continuar.")

# Iniciar bot
if __name__ == "__main__":
    init_db()
    print("🤖 Bot iniciado...")
    bot.infinity_polling()

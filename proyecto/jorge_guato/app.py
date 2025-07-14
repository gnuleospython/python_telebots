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

# --- Clases ---
class DBHelper:
    @staticmethod
    def init():
        with sqlite3.connect("chat.db") as conn:
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

    @staticmethod
    def guardar_pedido(user_id, datos):
        with sqlite3.connect("chat.db") as conn:
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

class PedidoManager:
    ESTADOS = {
        "MENU": "menu",
        "PEDIDO_NOMBRE": "nombre",
        "PEDIDO_TELEFONO": "telefono",
        "PEDIDO_EMAIL": "email",
        "PEDIDO_DIRECCION": "direccion"
    }

    PRODUCTOS = {
        "1": {"nombre": "Vino de Uva Premium", "precio": 25.00},
        "2": {"nombre": "Vino de Mortiño", "precio": 30.00},
        "3": {"nombre": "Vino de Arándano", "precio": 28.00},
        "4": {"nombre": "Chocolate Clásico", "precio": 8.00},
        "5": {"nombre": "Chocolate Premium", "precio": 12.00},
        "6": {"nombre": "Chocolate Especial", "precio": 15.00}
    }

    usuarios = {}

    @classmethod
    def reiniciar(cls, user_id):
        cls.usuarios[user_id] = {"estado": cls.ESTADOS["MENU"], "carrito": []}

    @classmethod
    def agregar_producto(cls, user_id, codigo):
        producto = cls.PRODUCTOS.get(codigo)
        if producto:
            cls.usuarios[user_id]["carrito"].append(producto)
            total = sum(p["precio"] for p in cls.usuarios[user_id]["carrito"])
            cls.usuarios[user_id]["pedido"] = {"productos": cls.usuarios[user_id]["carrito"], "total": total}
            cls.usuarios[user_id]["estado"] = cls.ESTADOS["PEDIDO_NOMBRE"]
            bot.send_message(user_id, f"🛒 {producto['nombre']} añadido al carrito.")
            bot.send_message(user_id, "👤 Ingresa tu nombre completo o escribe 0 para salir:")
        else:
            bot.send_message(user_id, "Producto no válido.")

# --- Bot Handlers ---
@bot.message_handler(commands=["start"])
def start(message: Message):
    user_id = message.from_user.id
    PedidoManager.reiniciar(user_id)

    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("1. Ver Catálogo de Vinos", "2. Ver Catálogo de Chocolates", "0. Salir")

    texto = """
👋 *¡Hola! Bienvenido a La Rústica* 🍷🍫

1. Ver Catálogo de Vinos
2. Ver Catálogo de Chocolates
0. Salir

Elige una opción:
    """
    bot.send_message(user_id, texto, reply_markup=markup, parse_mode="Markdown")

def mostrar_catalogo_vinos(user_id):
    texto = "🍷 *Catálogo de Vinos*\n"
    texto += "1. Vino de Uva Premium - $25.00\n"
    texto += "2. Vino de Mortiño - $30.00\n"
    texto += "3. Vino de Arándano - $28.00\n"
    texto += "\nEscribe el número del producto para seleccionarlo, o 0 para salir."
    bot.send_message(user_id, texto, parse_mode="Markdown")

def mostrar_catalogo_chocolates(user_id):
    texto = "🍫 *Chocolates La Rústica*\n"
    texto += "4. Chocolate Clásico - $8.00\n"
    texto += "5. Chocolate Premium - $12.00\n"
    texto += "6. Chocolate Especial - $15.00\n"
    texto += "\nEscribe el número del producto para seleccionarlo, o 0 para salir."
    bot.send_message(user_id, texto, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def handle_message(message: Message):
    user_id = message.from_user.id
    texto = message.text.strip()

    if user_id not in PedidoManager.usuarios:
        PedidoManager.reiniciar(user_id)

    if texto == "0":
        PedidoManager.reiniciar(user_id)
        bot.send_message(user_id, "❌ Proceso cancelado.")
        return start(message)

    estado = PedidoManager.usuarios[user_id]["estado"]

    if estado == PedidoManager.ESTADOS["MENU"]:
        if texto == "1. Ver Catálogo de Vinos":
            mostrar_catalogo_vinos(user_id)
        elif texto == "2. Ver Catálogo de Chocolates":
            mostrar_catalogo_chocolates(user_id)
        elif texto in PedidoManager.PRODUCTOS:
            PedidoManager.agregar_producto(user_id, texto)
        else:
            bot.send_message(user_id, "Por favor, selecciona una opción del menú.")

    elif estado == PedidoManager.ESTADOS["PEDIDO_NOMBRE"]:
        PedidoManager.usuarios[user_id]["pedido"]["nombre"] = texto
        PedidoManager.usuarios[user_id]["estado"] = PedidoManager.ESTADOS["PEDIDO_TELEFONO"]
        bot.send_message(user_id, "📞 Ingresa tu teléfono o escribe 0 para salir:")

    elif estado == PedidoManager.ESTADOS["PEDIDO_TELEFONO"]:
        PedidoManager.usuarios[user_id]["pedido"]["telefono"] = texto
        PedidoManager.usuarios[user_id]["estado"] = PedidoManager.ESTADOS["PEDIDO_EMAIL"]
        bot.send_message(user_id, "📧 Ingresa tu email o escribe 0 para salir:")

    elif estado == PedidoManager.ESTADOS["PEDIDO_EMAIL"]:
        PedidoManager.usuarios[user_id]["pedido"]["email"] = texto
        PedidoManager.usuarios[user_id]["estado"] = PedidoManager.ESTADOS["PEDIDO_DIRECCION"]
        bot.send_message(user_id, "📍 Ingresa tu dirección o escribe 0 para salir:")

    elif estado == PedidoManager.ESTADOS["PEDIDO_DIRECCION"]:
        PedidoManager.usuarios[user_id]["pedido"]["direccion"] = texto
        DBHelper.guardar_pedido(user_id, PedidoManager.usuarios[user_id]["pedido"])
        bot.send_message(user_id, "✅ Pedido guardado correctamente. Te contactaremos pronto. 🎉")
        PedidoManager.reiniciar(user_id)
        start(message)
    else:
        bot.send_message(user_id, "Usa el menú para continuar.")

# Iniciar bot
if __name__ == "__main__":
    DBHelper.init()
    print("🤖 Bot iniciado...")
    bot.infinity_polling()

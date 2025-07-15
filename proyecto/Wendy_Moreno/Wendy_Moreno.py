import os
import smtplib
from email.message import EmailMessage

import openpyxl
from telebot import TeleBot, types

# Configuración
TOKEN_BOT = '8130338428:AAFepXJ--dhup-dbLMpp_2ufU_kSwo48mJ8'
bot = TeleBot(TOKEN_BOT)

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'wendymorenoc2024@gmail.com'
SMTP_PASSWORD = 'qwwcjnppcclzzrwh'
DESTINATARIO = 'wendymorenoc2024@gmail.com'

EXCEL_FILE = 'mensajes_asesor.xlsx'

# Crear archivo Excel si no existe
def crear_archivo_excel():
    if not os.path.exists(EXCEL_FILE):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Mensajes"
        ws.append(["Cédula/RUC", "Nombre", "Teléfono", "Mensaje"])
        wb.save(EXCEL_FILE)

crear_archivo_excel()

# Estado de usuarios
estado_usuario = {}
datos_usuario = {}

@bot.message_handler(commands=['start'])
def start(message):
    texto = "👋 *Bienvenido a Tributa Bien*\n\n¿En qué te puedo ayudar hoy?"
    opciones = [
        "1️⃣ Apertura de RUC",
        "2️⃣ Declaración de IVA",
        "3️⃣ Declaración de RENTA",
        "4️⃣ Patente Municipal Quito",
        "5️⃣ Contactar a un Asesor"
    ]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for opcion in opciones:
        markup.add(opcion)
    bot.send_message(message.chat.id, texto, parse_mode="Markdown", reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def manejar_mensajes(message):
    chat_id = message.chat.id
    texto = message.text

    if chat_id in estado_usuario:
        paso = estado_usuario[chat_id]
        if paso == "cedula":
            datos_usuario[chat_id]["cedula"] = texto
            estado_usuario[chat_id] = "nombre"
            bot.send_message(chat_id, "📛 Escribe tu *nombre completo*:", parse_mode="Markdown")
        elif paso == "nombre":
            datos_usuario[chat_id]["nombre"] = texto
            estado_usuario[chat_id] = "telefono"
            bot.send_message(chat_id, "📱 Escribe tu *número de teléfono*:", parse_mode="Markdown")
        elif paso == "telefono":
            datos_usuario[chat_id]["telefono"] = texto
            estado_usuario[chat_id] = "mensaje"
            bot.send_message(chat_id, "📝 Escribe tu *mensaje* de consulta:", parse_mode="Markdown")
        elif paso == "mensaje":
            datos_usuario[chat_id]["mensaje"] = texto
            guardar_excel(datos_usuario[chat_id])
            enviar_email(datos_usuario[chat_id])
            bot.send_message(chat_id, "✅ ¡Mensaje enviado correctamente en breve un Asesor se comunicará contigo!")
            del estado_usuario[chat_id]
            del datos_usuario[chat_id]
        return

    if texto.startswith("1️⃣"):
        bot.send_message(chat_id, "📌 *Apertura de RUC*\n\nEn línea:\n- Firma electrónica\n- Cédula vigente\n- Factura de luz y agua\n- Correo electrónico\n- Monto de ventas\n- Actividad económica\n💵 Valor: 10 USD\n\nPresencial:\n- Autorización física firmada\n- Cédula\n- Dirección\n💵 Valor: 20 USD", parse_mode="Markdown")
    elif texto.startswith("2️⃣"):
        bot.send_message(chat_id, "📄 *Declaración de IVA*\n\n- Usuario y clave del SRI\n- Facturas de compras y ventas\n💵 Valor: según facturación", parse_mode="Markdown")
    elif texto.startswith("3️⃣"):
        bot.send_message(chat_id, "💰 *Declaración de RENTA*\n\n- Usuario y clave del SRI\n- Régimen y facturación\n💵 Valor: 20 USD", parse_mode="Markdown")
    elif texto.startswith("4️⃣"):
        bot.send_message(chat_id, "🏢 *Patente Municipal Quito*\n\n- Usuario y clave\n- Firma electrónica si aplica\n💵 Valor: 5 a 10 USD", parse_mode="Markdown")
    elif texto.startswith("5️⃣"):
        bot.send_message(chat_id, "📞 *Contactar a un Asesor*\n\nPor favor ingresa tu *cédula o RUC* para iniciar:", parse_mode="Markdown")
        estado_usuario[chat_id] = "cedula"
        datos_usuario[chat_id] = {}
    else:
        bot.send_message(chat_id, "❗ Usa el menú para elegir una opción válida.")

def guardar_excel(datos):
    try:
        crear_archivo_excel()
        wb = openpyxl.load_workbook(EXCEL_FILE)
        ws = wb.active
        ws.append([
            datos['cedula'],
            datos['nombre'],
            datos['telefono'],
            datos['mensaje']
        ])
        wb.save(EXCEL_FILE)
        print("✅ Mensaje guardado en Excel.")
    except Exception as e:
        print(f"❌ Error al guardar en Excel: {e}")

def enviar_email(datos):
    try:
        msg = EmailMessage()
        msg['Subject'] = f"Nuevo mensaje de {datos['nombre']} - {datos['cedula']}"
        msg['From'] = SMTP_USER
        msg['To'] = DESTINATARIO

        cuerpo = (
            f"Cédula o RUC: {datos['cedula']}\n"
            f"Nombre: {datos['nombre']}\n"
            f"Teléfono: {datos['telefono']}\n"
            f"Mensaje:\n{datos['mensaje']}\n\n"
            f"✅ Autorización para uso de datos otorgada por el usuario."
        )
        msg.set_content(cuerpo)

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        print("📧 Correo enviado con éxito, en breve el Asesor se pondrá en contacto contigo.")
    except Exception as e:
        print(f"❌ Error al enviar correo: {e}")

if __name__ == '__main__':
    print("🤖 Bot ejecutándose...")
    bot.infinity_polling()

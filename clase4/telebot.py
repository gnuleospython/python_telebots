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

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_URL = os.getenv("MAILJET_URL")
MAILJET_API_SECRET = os.getenv("MAILJET_SECRET_KEY")
MAILJET_FROM_NAME = os.getenv("MAILJET_FROM_NAME")
EMAIL_FROM = os.getenv("EMAIL_FROM")

MENU, DATOS, AUTORIZACION, CONFIRMAR, ACCION = range(4)

SERVICIOS = {
    "1. 🌐 Web App": 1000,
    "2. 📱 Mobile App": 1200,
    "3. 🔌 API REST": 800,
    "4. 📋 Consultoría": 500
}

conn = sqlite3.connect("telebot_complete.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    servicio TEXT,
    message_id INTEGER,
    timestamp TEXT
)
""")
conn.commit()

def guardar_interaccion(update: Update):
    user = update.effective_user
    username = user.username or "Sin username"
    servicio = update.message.text
    message_id = update.message.message_id
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO chat_data (user_id, username, servicio, message_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, username, servicio, message_id, timestamp))
    conn.commit()

# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🚀 Bienvenido al *Bot de Servicios de Software*.\n\n"
        "Por favor, selecciona un servicio de la lista:"
    )
    keyboard = [[opcion] for opcion in SERVICIOS.keys()]
    await update.message.reply_text(
        mensaje,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    guardar_interaccion(update)
    return MENU

# Selección del servicio
async def seleccionar_servicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servicio = update.message.text.strip()
    if servicio in SERVICIOS:
        context.user_data["servicio"] = servicio
        await update.message.reply_text(
            f"📝 Has seleccionado *{servicio}*.\n\nAhora escribe:\n1. Tu nombre completo\n2. Tu correo electrónico\n3. Una breve descripción del proyecto",
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return DATOS
    else:
        await update.message.reply_text("❌ Opción inválida. Selecciona un servicio del menú.")
        return await start(update, context)

# Recolección de datos
async def recibir_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    email = extraer_email(texto)
    if not email:
        await update.message.reply_text(
            "❌ No se detectó un correo válido.\nPor favor, escribe tus datos nuevamente en este formato:\n\n`Nombre - correo@ejemplo.com - descripción`",
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return DATOS

    context.user_data["datos"] = texto
    keyboard = [["✅ Sí", "❌ No"]]
    await update.message.reply_text(
        "🔐 ¿Autorizas el uso de tus datos para contactarte y procesar tu pedido?\nSelecciona una opción: \n✅ Sí / ❌ No",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    guardar_interaccion(update)
    return AUTORIZACION

async def autorizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.lower()
    if "sí" in respuesta or "si" in respuesta or "✅" in respuesta:
        servicio = context.user_data["servicio"]
        precio = SERVICIOS[servicio]
        keyboard = [["✅ Confirmar", "❌ Cancelar"]]
        await update.message.reply_text(
            f"💰 El precio de *{servicio}* es de *${precio}*.\n\n¿Deseas confirmar el pedido?\n✅ Confirmar / ❌ Cancelar",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return CONFIRMAR
    elif "no" in respuesta or "❌" in respuesta:
        await update.message.reply_text("🚫 No podemos continuar sin tu autorización. Escribe /start para comenzar de nuevo.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Respuesta inválida. Selecciona *Sí* o *No* desde el menú.")
        return AUTORIZACION

# Confirmación del pedido
async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    guardar_interaccion(update)
    if "confirmar" in texto or "✅" in texto:
        servicio = context.user_data["servicio"]
        descripcion = context.user_data["datos"]
        precio = SERVICIOS[servicio]
        correo = extraer_email(descripcion)

        mensaje = (
            f"🎉 *Gracias por tu pedido!*\n\n"
            f"✅ *Servicio:* {servicio}\n"
            f"📝 *Descripción:* {descripcion}\n"
            f"💵 *Precio:* ${precio}\n\n"
            "Nos pondremos en contacto contigo pronto. 📧"
        )
        
        print("email", descripcion, precio, correo)
        print("mensaje", mensaje)

        if correo:
            enviado = enviar_mailjet(context, correo, MAILJET_FROM_NAME + " Confirmación de tu pedido", mensaje)
            if enviado:
                await update.message.reply_text("📧 Correo de confirmación enviado con éxito ✅")
            else:
                await update.message.reply_text("⚠️ Hubo un error al enviar el correo.")
        else:
            await update.message.reply_text("⚠️ El correo no se detectó correctamente. No se envió el correo.")

        await update.message.reply_text("¿Necesitas algo más? Escribe /start para hacer otro pedido.")
        return ConversationHandler.END
    elif "cancelar" in texto or "❌" in texto:
        await update.message.reply_text("❌ Pedido cancelado. Si deseas iniciar de nuevo, escribe /start.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Respuesta inválida. Selecciona *Confirmar* o *Cancelar* desde el menú.")
        return MENU

# Extraer correo desde un texto
def extraer_email(texto):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
    return match.group(0) if match else None

def enviar_mailjet(context, destinatario, asunto, contenido):
    # data = {
    #     'Messages': [
    #         {
    #             "From": {
    #                 "Email": EMAIL_FROM, 
    #                 "Name": "Servicios de Software"
    #             },
    #             "To": [
    #                 {
    #                     "Email": destinatario,
    #                     "Name": "Cliente"
    #                 }
    #             ],
    #             "Subject": asunto,
    #             "TextPart": contenido
    #         }
    #     ]
    # }
    
    data = {
        "Messages": [
            {
                "From": {
                    "Email": os.getenv("EMAIL_FROM"),
                    "Name": "Servicios de Software"
                },
                "To": [
                    {
                        "Email": destinatario,
                        "Name": "Cliente"
                    }
                ],
                "Subject": asunto,
                "HTMLPart": f"""
                    <div style="font-family:Arial, sans-serif; color:#2c3e50;">
                        <h2>🎉 ¡Gracias por tu pedido!</h2>
                        <p>✅ <strong>Servicio:</strong> {context.user_data['servicio']}</p>
                        <p>📝 <strong>Descripción:</strong> {context.user_data['datos']}</p>
                        <p>💵 <strong>Precio:</strong> ${SERVICIOS[context.user_data['servicio']]}</p>

                        <img src="https://via.placeholder.com/500x200.png?text=Gracias+por+tu+confianza" 
                            alt="Gracias por tu pedido" 
                            style="width:100%; max-width:500px; margin:20px 0;">

                        <p>Haz clic en el botón para visitar nuestra página:</p>
                        <a href="https://www.splendercode.com/"
                        style="display:inline-block; padding:12px 24px; background-color:#1abc9c; color:white; text-decoration:none; border-radius:6px; font-weight:bold;">
                        Ir a la página 🚀
                        </a>

                    </div>
                """
            }
        ]
    }

    try:
        response = requests.post(
            MAILJET_URL,
            json=data,
            auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
            timeout=(3.05, 5)
        )
        print(f"📨 Mailjet response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error enviando correo con Mailjet: {e}")
        return False

# Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, seleccionar_servicio)],
            DATOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos)],
            AUTORIZACION: [MessageHandler(filters.TEXT & ~filters.COMMAND, autorizacion)],
            CONFIRMAR: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()

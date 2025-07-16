from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup
)
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters, ConversationHandler
)
import requests
import os
import re
import sqlite3
from datetime import datetime
from dotenv import load_dotenv

# 📌 Cargar .env
load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_URL = os.getenv("MAILJET_URL")
EMAIL_FROM = os.getenv("EMAIL_FROM")

# 📌 Estados
MENU, DATOS, AUTORIZACION, CONFIRMAR = range(4)

# 📌 Servicios de Bodega Palermo
SERVICIOS = {
    "🍷 Vinos": 25,
    "🥃 Licores": 30,
    "🍺 Cervezas": 15,
    "🍾 Espumantes": 40
}

# 📌 Base de datos
conn = sqlite3.connect("bodega_palermo.db", check_same_thread=False)
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
    servicio = ""
    message_id = None

    if update.callback_query:
        servicio = update.callback_query.data
        message_id = update.callback_query.message.message_id
    elif update.message:
        servicio = update.message.text
        message_id = update.message.message_id

    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO chat_data (user_id, username, servicio, message_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, username, servicio, message_id, timestamp))
    conn.commit()

# 📌 Inicio con menú interactivo
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🍷 *Bienvenido a Bodega Palermo* 🍾\n\n"
        "Selecciona el producto que deseas consultar por favor:"
    )
    keyboard = [
        [InlineKeyboardButton(text=opcion, callback_data=opcion)]
        for opcion in SERVICIOS.keys()
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        mensaje,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return MENU

# 📌 Selección del producto
async def servicio_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    servicio = query.data
    context.user_data["servicio"] = servicio

    await query.message.reply_text(
        f"📋 Has seleccionado *{servicio}*.\n\n"
        f"Por favor, indícanos:\n1. Tu nombre completo\n2. Tu correo electrónico\n3. Detalles del pedido",
        parse_mode="Markdown"
    )
    guardar_interaccion(update)
    return DATOS

# 📌 Recolección de datos
async def recibir_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    email = extraer_email(texto)
    if not email:
        await update.message.reply_text(
            "❌ No detectamos un correo válido.\nPor favor escribe:\n`Nombre - correo@ejemplo.com - detalles del pedido`",
            parse_mode="Markdown"
        )
        return DATOS

    context.user_data["datos"] = texto

    await update.message.reply_text(
        "🔐 ¿Autorizas a Bodega Palermo a usar tus datos para procesar tu pedido?",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Sí", callback_data="si")],
            [InlineKeyboardButton("❌ No", callback_data="no")]
        ])
    )
    guardar_interaccion(update)
    return AUTORIZACION

# 📌 Autorización
async def autorizacion_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    respuesta = query.data.lower()

    if "si" in respuesta:
        servicio = context.user_data["servicio"]
        precio = SERVICIOS[servicio]
        await query.message.reply_text(
            f"💵 El precio estimado de *{servicio}* es de *${precio}* por unidad.\n\n¿Deseas confirmar tu pedido?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("✅ Confirmar", callback_data="confirmar")],
                [InlineKeyboardButton("❌ Cancelar", callback_data="cancelar")]
            ])
        )
        guardar_interaccion(update)
        return CONFIRMAR
    else:
        await query.message.reply_text(
            "🚫 No podemos continuar sin tu autorización.\nUsa /start para iniciar de nuevo."
        )
        return ConversationHandler.END

# 📌 Confirmación
async def confirmar_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    accion = query.data.lower()

    if "confirmar" in accion:
        servicio = context.user_data["servicio"]
        descripcion = context.user_data["datos"]
        precio = SERVICIOS[servicio]
        correo = extraer_email(descripcion)

        mensaje = (
            f"🍷 *Bodega Palermo* 🍾\n\n"
            f"✅ *Producto:* {servicio}\n"
            f"📝 *Detalles:* {descripcion}\n"
            f"💵 *Precio estimado:* ${precio}\n\n"
            "Nos pondremos en contacto contigo pronto. ¡Gracias por tu pedido!"
        )

        if correo:
            enviado = enviar_mailjet(context, correo, f"Confirmación de pedido - Bodega Palermo", mensaje)
            if enviado:
                await query.message.reply_text("📧 Correo de confirmación enviado ✅")
            else:
                await query.message.reply_text("⚠️ Ocurrió un error al enviar el correo.")
        else:
            await query.message.reply_text("⚠️ Correo no detectado correctamente.")

        await query.message.reply_text("🍾 Si deseas realizar otro pedido, usa /start.")
        guardar_interaccion(update)
        return ConversationHandler.END

    else:
        await query.message.reply_text(
            "❌ Pedido cancelado. Usa /start para comenzar de nuevo cuando quieras."
        )
        return ConversationHandler.END

# 📌 Extraer correo
def extraer_email(texto):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
    return match.group(0) if match else None

# 📌 Enviar correo
def enviar_mailjet(context, destinatario, asunto, contenido):
    data = {
        "Messages": [
            {
                "From": {"Email": EMAIL_FROM, "Name": "Bodega Palermo"},
                "To": [{"Email": destinatario}],
                "Subject": asunto,
                "TextPart": contenido
            }
        ]
    }
    try:
        response = requests.post(
            MAILJET_URL,
            json=data,
            auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY)
        )
        print(f"Mailjet: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# 📌 Main
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [CallbackQueryHandler(servicio_callback)],
            DATOS: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos)],
            AUTORIZACION: [CallbackQueryHandler(autorizacion_callback)],
            CONFIRMAR: [CallbackQueryHandler(confirmar_callback)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("🍾 Bot Bodega Palermo en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()

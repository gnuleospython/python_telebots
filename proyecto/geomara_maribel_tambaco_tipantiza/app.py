from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes,
    filters, ConversationHandler
)
import sqlite3
import os
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
MAILJET_URL = os.getenv("MAILJET_URL")
MAILJET_FROM_NAME = os.getenv("MAILJET_FROM_NAME")
EMAIL_FROM = os.getenv("EMAIL_FROM")

MENU, DATOS, AUTORIZACION, CONFIRMAR = range(4)

# Cursos de capacitación que ofrece  KonKito
CURSOS = {
    "1. 📈 Marketing Digital para Emprendedores": 300,
    "2. 💼 Gestión Financiera Básica": 250,
    "3. 🚀 Estrategias de Crecimiento": 350,
    "4. 🛠️ Herramientas para la Productividad": 200
}

conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    curso TEXT,
    message_id INTEGER,
    timestamp TEXT
)
""")
conn.commit()

def guardar_interaccion(update: Update):
    user = update.effective_user
    username = user.username or "Sin username"
    texto = update.message.text
    message_id = update.message.message_id
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO chat_data (user_id, username, curso, message_id, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, username, texto, message_id, timestamp))
    conn.commit()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        "🚀 Bienvenido al *Bot de Cursos de capacitación de KonKito*.\n\n"
        "Selecciona un curso para continuar:"
    )
    keyboard = [[curso] for curso in CURSOS.keys()]
    await update.message.reply_text(
        mensaje,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    guardar_interaccion(update)
    return MENU

async def seleccionar_curso(update: Update, context: ContextTypes.DEFAULT_TYPE):
    curso = update.message.text.strip()
    if curso in CURSOS:
        context.user_data["curso"] = curso
        await update.message.reply_text(
            "✍️ Por favor, escribe:\n1. Tu nombre completo\n2. Tu correo electrónico\n3. Una breve descripción de tu emprendimiento\n\nFormato:\n`Vilma Pérez - correo@ejemplo.com - Información de . . .`",
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return DATOS
    else:
        await update.message.reply_text("❌ Opción inválida. Usa el menú para elegir un curso.")
        return MENU

async def recibir_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    email = extraer_email(texto)
    if not email:
        await update.message.reply_text(
            "❌ No se detectó un correo válido. Escribe tus datos así:\n`Nombre - correo@ejemplo.com - descripción`",
            parse_mode="Markdown"
        )
        return DATOS

    context.user_data["datos"] = texto
    keyboard = [["✅ Sí", "❌ No"]]
    await update.message.reply_text(
        "🔐 ¿Autorizas el uso de tus datos para contactarte y procesar tu inscripción?",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    guardar_interaccion(update)
    return AUTORIZACION

async def autorizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.lower()
    if "sí" in respuesta or "si" in respuesta or "✅" in respuesta:
        curso = context.user_data["curso"]
        precio = CURSOS[curso]
        keyboard = [["✅ Confirmar", "❌ Cancelar"]]
        await update.message.reply_text(
            f"💰 El precio del curso *{curso}* es de *${precio}*.\n¿Deseas confirmar tu inscripción?",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
            parse_mode="Markdown"
        )
        return CONFIRMAR
    elif "no" in respuesta or "❌" in respuesta:
        await update.message.reply_text("🚫 No podemos continuar sin tu autorización. Escribe /start para reiniciar.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("❌ Respuesta no válida. Usa el menú.")
        return AUTORIZACION

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    if "confirmar" in texto or "✅" in texto:
        curso = context.user_data["curso"]
        descripcion = context.user_data["datos"]
        correo = extraer_email(descripcion)

        mensaje = (
            f"🎉 *Gracias por inscribirte!*\n\n"
            f"✅ *Curso:* {curso}\n"
            f"📝 *Descripción:* {descripcion}\n"
            f"💵 *Precio:* ${CURSOS[curso]}\n\n"
            "Nos pondremos en contacto contigo pronto. 📧"
        )

        enviado = enviar_mailjet(context, correo, "Confirmación de inscripción", mensaje)
        if enviado:
            await update.message.reply_text("📧 Correo de confirmación enviado con éxito.")
        else:
            await update.message.reply_text("⚠️ Hubo un error al enviar el correo.")

        await update.message.reply_text("¿Necesitas algo más? Escribe /start para comenzar otra inscripción.")
        return ConversationHandler.END

    elif "cancelar" in texto or "❌" in texto:
        await update.message.reply_text("❌ Inscripción cancelada. Escribe /start para iniciar de nuevo.")
        return ConversationHandler.END

    else:
        await update.message.reply_text("❌ Respuesta inválida. Usa el menú.")
        return CONFIRMAR

def extraer_email(texto):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
    return match.group(0) if match else None

def enviar_mailjet(context, destinatario, asunto, contenido):
    data = {
        "Messages": [
            {
                "From": {
                    "Email": EMAIL_FROM,
                    "Name": MAILJET_FROM_NAME
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
                        <h2>🎉 ¡Gracias por tu inscripción!</h2>
                        <p>✅ <strong>Curso:</strong> {context.user_data['curso']}</p>
                        <p>📝 <strong>Descripción:</strong> {context.user_data['datos']}</p>
                        <p>💵 <strong>Precio:</strong> ${CURSOS[context.user_data['curso']]}</p>
                        <p>Nos pondremos en contacto contigo pronto.</p>
                    </div>
                """
            }
        ]
    }

    try:
        response = requests.post(
            MAILJET_URL,
            json=data,
            auth=(MAILJET_API_KEY, MAILJET_SECRET_KEY),
            timeout=(3.05, 5)
        )
        print(f"Mailjet response: {response.status_code} - {response.text}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error enviando correo con Mailjet: {e}")
        return False

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, seleccionar_curso)],
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

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  mitelegrambotTopograf.py
#  
#  Copyright 2025 Edison TANA <oefica@disroot.org>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  Desarrollado en GNU_Linux


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
import logging
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
api_key = os.getenv('MAILJET_API_KEY')
api_secret = os.getenv('MAILJET_SECRET_KEY')

correoremite = os.getenv('EMAIL_REMITENTE')
correodestino = os.getenv('EMAIL_DESTINATARIO')


MAIN_MENU, FIRST_MENU, SECOND_MENU, THIRD_MENU = range(4)

SERVICIOS = {
    "1. 🗺️ Modelos de terreno en 3D": 100,
    "2. 📏 Nivelaciones y replanteos": 12,
    "3. 🌎 Levantamientos topograficos": 180,
    "4. 👨 Asesoría topografica": 60
}

conn = sqlite3.connect("mibase.db", check_same_thread=False)
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
    message_id = update.message.message_id    
    servicio = update.message.text
    timestamp = datetime.now().isoformat()

    cursor.execute("""
        INSERT INTO chat_data (user_id, message_id, username, servicio, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (user.id, username, servicio, message_id, timestamp))
    conn.commit()

# Extraer correo desde un texto
def extraer_email(texto):
    match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', texto)
    return match.group(0) if match else None

def enviarcorreos(context, correodestino, asunto, contenido):
    
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
        'Messages': [
            {
                "From": {
                    "Email": correoremite,  # Remove $ and use variable directly
                    "Name": "Info EuatorTopografia"
                },
                "To": [
                    {
                        "Email": correodestino,  # Remove $ and use variable directly
                        "Name": "Cliente de equatortopografia " 
                    }
                ],
                "Subject": asunto,
                "TextPart": "Saludos desde Topografia!",
                "HTMLPart": f"""
                    <h3>Estimado usuario, bienvenido a  <a href=\"https://equatortopografia-83bf40.frama.io/\">EquatorTopografia</a>!</h3><br />Un gusto conectar con usted!
                    <div>
                        <p> <strong>Usted ha elegido el servicio de:</strong> </p>
                        <ul>
                        <li>
                        <p>{context.user_data['servicio']} </p>
                        </li>
                        <li>Su detalle es {context.user_data['datos']}</li>
                        <li>Su costo es ${SERVICIOS[context.user_data['servicio']]}</li>
                        </ul>                        
                        <br>                        
                        Gracias por escribirnos, hasta pronto.
                        <hr>
                        <h4>Más servicios</h4>
                        <br>
                        <ol>
                        <li>Modelos de terreno en 3D</li>
                        <li>Levantamientos topograficos</li>
                        <li>
                        <p>Nivelaciones y replanteos con precision topografica</p>
                        </li>
                        <li>
                        <p>Georeferenciaciones</p>
                        </li>
                        <li>
                        <p>Digitalización topografica</p>
                        </li>
                        </ol>                         
                    </div>
                    <br>
                    <p>Contacta por telegram con nuestro asesor en <a href="https://t.me/leosAcadUIO">t.me/leosAcadUIO</a></p>
                    """
            }
        ]
    }

    result = mailjet.send.create(data=data)
    print(result.status_code)
    print('Ok')

    
# Inicio del bot
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensaje = (
        """
        Hola. Buen día \n 🌟 Bienvenido/a a AsistenteBot!  (@academicobot) 🌟.\n          
          ______________________________________
        < Te ayudamos en soporte y asesoría de >
         -----------------------------------------------------------------------

        A continuacion elige un ítem de la lista:
        """
    )
    keyboard = [[opcion] for opcion in SERVICIOS.keys()]
    await update.message.reply_text(
        mensaje,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
        parse_mode="Markdown"
    )
    guardar_interaccion(update)
    return MAIN_MENU

# Selección del servicio
async def seleccionar_servicio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    servicio = update.message.text.strip()
    if servicio in SERVICIOS:
        context.user_data["servicio"] = servicio
        await update.message.reply_text(
            f"📝 Has seleccionado *{servicio}*.\n\nPor favor, digita su:\n1. Nombre completo\n2. Correo electrónico\n3. Una breve detalle de su caso:",
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return FIRST_MENU
    else:
        await update.message.reply_text("Opción inválida. Selecciona un servicio del menú.")
        return await start(update, context)


# Recolección de datos
async def recibir_datos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip()
    email = extraer_email(texto)
    if not email:
        await update.message.reply_text(
            "Se encontró un error.\n De nuevo ingrese su informacion de acuerdo a este formato:\n\n`Nombre - correo@ejemplo.com - detalle`",
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return FIRST_MENU

    context.user_data["datos"] = texto
    keyboard = [["Sí", "No"]]
    await update.message.reply_text(
        " Autorizo a EquatorTopografia a verificar la autenticidad de la información proporcionada y utilizarla para fines informativos. Entiendo que mis datos serán tratados conforme a la Ley de Protección de Datos Personales de EC.: \n SI / NO",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )
    guardar_interaccion(update)
    return SECOND_MENU

async def autorizacion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    respuesta = update.message.text.lower()
    # Fix: Remove redundant 'in respuesta' checks
    if "si" in respuesta or "sí" in respuesta:
        servicio = context.user_data["servicio"]
        precio = SERVICIOS[servicio]
        keyboard = [["✅ Confirmar", "❌ Cancelar"]]
        await update.message.reply_text(
            f"El *{servicio}* tiene un costo de *${precio}*.\n\n¿Deseas confirmar el pedido?\n Confirmar / Cancelar",
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True),
            parse_mode="Markdown"
        )
        guardar_interaccion(update)
        return THIRD_MENU
    elif "no" in respuesta:
        await update.message.reply_text("No podemos continuar sin tu autorización. Escribe /start para comenzar de nuevo.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Respuesta inválida. Selecciona *Sí* o *No* desde el menú.")
        return SECOND_MENU

async def confirmar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.lower()
    guardar_interaccion(update)
    # A
    if "confirmar" in texto:
        servicio = context.user_data["servicio"]
        detalle = context.user_data["datos"]
        precio = SERVICIOS[servicio]
        correo = extraer_email(detalle)
        correodestinos = correo
        
        mensaje = (
            f"*Gracias por tu pedido!*\n\n"
            f"*Servicio:* {servicio}\n"
            f"*Detalle:* {detalle}\n"
            f"*Precio:* ${precio}\n\n"
            "Nos pondremos en contacto contigo pronto. 📧"
        )
        
        # Optional: Add logging instead of print statements
        logging.info(f"Email: {detalle}, Precio: {precio}, Correo: {correo}")
        logging.info(f"Mensaje: {mensaje}")

        if correo:
            try:
                enviado = enviarcorreos(context, correodestinos, ":) Info sobre cotizacion para "+correo, mensaje)
                await update.message.reply_text("Correo enviado exitosamente.")
            except Exception as e:
                logging.error(f"Error enviando correo: {e}")
                await update.message.reply_text("Hubo un problema al enviar el correo.")
        else:
            await update.message.reply_text("Correo NO enviado")

        await update.message.reply_text("¿Requieres cotizarotro servicio? Digita /start para volver al menú principal")
        return ConversationHandler.END
    elif "cancelar" in texto or texto == "❌":
        await update.message.reply_text("Servicio cancelado. Si deseas iniciar de nuevo, escribe /start.")
        return ConversationHandler.END
    else:
        await update.message.reply_text("Respuesta inválida. Selecciona *Confirmar* o *Cancelar* desde el menú.")
        return THIRD_MENU  # Fix: Return to THIRD_MENU instead of MAIN_MENU


            
# Mi funcion pincipal
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            MAIN_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, seleccionar_servicio)],
            FIRST_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_datos)],
            SECOND_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, autorizacion)],
            THIRD_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirmar)],
        },
        fallbacks=[],
    )

    app.add_handler(conv_handler)
    print("mi bot ejecutandose")
    app.run_polling()

if __name__ == "__main__":
    main()

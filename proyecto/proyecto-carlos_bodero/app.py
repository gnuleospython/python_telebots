import os
import google.generativeai as genai
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base, sessionmaker

# Carga variables de entorno
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY_GEMINI")
USUARIO_CORREO = os.getenv("USUARIO_CORREO")
CONTRASENA_CORREO = os.getenv("CONTRASENA_CORREO")


if not GEMINI_API_KEY:
    raise Exception("La API Key de Gemini no está configurada en el archivo .env.")


modelo_en_uso = None

modelos = [
    "gemini-2.5-flash",
    "gemini-2.5-flash-latest", 
    "gemini-2.5-flash-002",   
    "gemini-2.5-pro",
    "gemini-2.5-pro-latest",  
    "gemini-2.5-pro-002",   
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-1.5-flash-002",
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-pro-002",
]

# Datos de tu cuenta Gmail
usuario_mail =  USUARIO_CORREO
contrasena = CONTRASENA_CORREO

genai.configure(api_key=GEMINI_API_KEY)
modelo_en_uso = modelos[0]

# Flask y DB setup
app = Flask(__name__)
#DATABASE_URL = "sqlite:///chat.db"
DATABASE_URL = "sqlite:///proyecto/proyecto-carlos_bodero/chat.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

# Modelo de Chat
class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    usuario_nombre = Column(String(100))
    correo = Column(String(100))
    texto = Column(Text)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

def consultar_gemini(mensaje):
    model = genai.GenerativeModel(modelo_en_uso)
    try:
        response = model.generate_content(mensaje)
        return response.text
    except Exception as e:
        return f"Error consultando Gemini: {str(e)}"

def enviarCorreo(usuario,correo,mensaje):
    # Configuración del mensaje
    msg = EmailMessage()
    msg['Subject'] = "Chat " + str(usuario)
    msg['From'] = 'monitorcbo4@gmail.com'
    msg['To'] = str(correo)
    msg.set_content(mensaje)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(usuario_mail, contrasena)
            smtp.send_message(msg)
            print("Correo enviado correctamente.")
    except Exception as e:
        print("Error al enviar el correo:", e)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message")
    respuesta_gemini = consultar_gemini(user_message)
    return jsonify({"response": respuesta_gemini})

@app.route("/guardar", methods=["POST"])
def guardar():
    data = request.json
    nombre = data.get("nombre")
    correo = data.get("email")
    texto_chat = data.get("chat")
    chat_entry = Chat(usuario_nombre=nombre, correo=correo, texto=texto_chat)
    db_session.add(chat_entry)
    db_session.commit()
    enviarCorreo(nombre,correo,texto_chat)
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run("0.0.0.0",debug=True)

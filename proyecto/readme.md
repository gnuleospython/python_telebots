# 🧠 Proyecto Final – Chatbot con Python

## 🚀 Descripción General

    Este proyecto tiene como objetivo aplicar todos los conocimientos adquiridos durante el curso, desarrollando un chatbot funcional que puede ejecutarse en Telegram o desde una interfaz web utilizando Flask. El bot debe conectarse a una API de inteligencia artificial (como Gemini) y almacenar sus interacciones en una base de datos. Además, debe incluir una acción adicional como enviar correos, generar una imagen o exportar información.

## 🎯 Objetivo del Proyecto

    Crear un chatbot inteligente que interactúe con usuarios, responda preguntas, tome decisiones o realice acciones específicas (como agendar una cita, enviar un mensaje de confirmación o generar una imagen). Puedes elegir una de estas dos opciones:

### Opción 1 – 🤖 Bot de Telegram

    Desarrolla un chatbot en Telegram usando `python-telegram-bot` que:
    - Salude al usuario
    - Ofrezca un menú de servicios
    - Tome datos de contacto o pedidos
    - Envíe mensajes de confirmación o genere imágenes
    - Guarde las conversaciones en SQLite o JSON

### Opción 2 – 🌐 Web App con Flask

    Crea una aplicación SPA (Single Page App) que:
    - Permita al usuario enviar preguntas
    - Se conecte con una IA (Gemini API, HuggingFace, etc.)
    - Muestre respuestas como un chat web
    - Guarde las conversaciones en SQLite
    - Permita limpiar el historial y generar confirmaciones

    ---

## 📁 Organización del Proyecto

    1. Dentro de la carpeta `proyecto`, crea una carpeta con tu nombre y apellido.

    proyecto/
    ├── nombre_apellido/
    │   ├── app.py
    │   ├── templates/
    │   │   └── index.html (solo para Flask)
    │   ├── static/
    │   │   └── styles.css (opcional) o puedes usar Boostrap
    │   ├── chat.db
    │   ├── .env
    │   └── README.md


    2. Coloca tu código y recursos dentro de esa carpeta.
    3. Indica claramente en tu `README.md` qué opción desarrollaste (Telegram o Flask).

    ---

## 🧰 Requisitos Generales

### Librerías Comunes (para ambos proyectos)

    ```bash
        pip install python-dotenv
    ```

## 🚀 Opción 1: Telegram Bot

### 🧩 Librerías necesarias

    ```bash
        pip install python-telegram-bot
        pip install python-dotenv
    ```

### 🔐 .env (ejemplo)

    ```bash
        TELEGRAM_BOT_TOKEN=tu_token_de_telegram
    ```

### 📌 Pasos

    1. **Crea tu bot en Telegram** usando [@BotFather](https://t.me/BotFather) y obtén tu token.
    2. **Instala las dependencias necesarias**:

    ```bash
    pip install python-telegram-bot python-dotenv sqlite3
    ```

    3. **Crea un archivo .env y agrega tu token**:

    ```bash
        TELEGRAM_BOT_TOKEN=TU_TOKEN_AQUI
    ```

    4. **Guardar cada interacción en SQLite (usuario, mensaje, hora)**.

    5. **Agregar una acción adicional:**

    6. **Enviar correo de confirmación**

    7. **Generar imagen o PDF**

## 🚀 Opción 2: Flask + AI

### 🧩 Librerías necesarias

    ```bash
        pip install Flask google-generativeai python-dotenv
    ```

### 🔐 .env (ejemplo)

    ```bash
        API_KEY_GEMINI=tu_clave_api_gemini
    ```

### 📌 Pasos

    1. **Crear entorno virtual:** 

    ```bash
        python -m venv venv
        source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

    2. **Crear archivo app.py y cargar la clave desde .env**:

    3. **Crear formularios HTML + Bootstrap para enviar mensajes**:

    4. **Procesar las preguntas con Gemini y mostrar respuestas.**

    5. **Guardar los mensajes en SQLite**

    6. **Agregar acción adicional:**

    7. **Generar imagen o PDF, enviar correo**

## ✅ Requisitos para Aprobar

| Requisito                             | Obligatorio |
|--------------------------------------|-------------|
| Chat funcional                       | ✅         |
| Conexión con API externa             | ✅         |
| Base de datos funcional              | ✅         |
| Acción extra (correo, imagen, etc.) | ✅         |
| Documentación en README.md           | ✅         |
| Carpeta con nombre del estudiante    | ✅         |

---

## 📰 Entrega

1. Crear una carpeta con tu nombre completo en la carpeta `proyecto/`.
2. Agregar código fuente, plantilla HTML (si aplica), `.env.example`, base de datos y `README.md`.
3. Hacer fork del repositorio oficial.
4. Subir tus cambios (commit & push).
5. Crear Pull Request con el título:
   > Proyecto - TuNombre TuApellido

---

## 🚀 Recomendaciones

- Investiga APIs gratuitas para mejorar tu bot (HuggingFace, Fun Translations, etc.).
- Usa `flask-mail` para enviar correos desde Flask.
- Usa `sqlite3`, `pandas`, `reportlab` o `Pillow` para guardar y mostrar datos.
- Usa `dotenv` para evitar exponer tus tokens.
- Agrega paginación, exportación o estilo profesional a tu app.

---

## 📈 Inspiración

Este proyecto te prepara para desarrollar sistemas reales de atención al cliente, asistentes inteligentes o integraciones en aplicaciones productivas.

Pon en práctica tus conocimientos de Python, APIs, bases de datos, interfaces y comunicación con usuarios.

---

✨ ¡Mucho éxito y manos al código! ✨

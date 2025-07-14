# Chat Gemini con Flask y SQLite

Este proyecto es una aplicación web de chat construida con **Flask** que permite interactuar con la IA de **Gemini** (Google). La aplicación almacena cada conversación en una base de datos **SQLite**, guardando el nombre, correo electrónico del usuario y el historial del chat.

---

## Características

- Interfaz web amigable para chatear con Gemini.
- Campos para ingresar **nombre** y **correo electrónico** del usuario.
- Al finalizar la conversación, se almacena todo el chat en SQLite.
- Integración con la API oficial de Gemini (`google-generativeai`).

---

## Requisitos

- Python 3.8 o superior
- Cuenta de Google para obtener la API Key de Gemini

---

## Instalación

1. **Clona este repositorio** o descarga el código.

2. **Instala las dependencias**:

    ```bash
    pip install flask google-generativeai python-dotenv sqlalchemy
    ```

3. **Obtén tu API Key de Gemini**:

    - Accede a [Google AI Studio](https://aistudio.google.com/app/apikey)
    - Inicia sesión con tu cuenta Google
    - Haz clic en “Create API key” y copia el valor

4. **Configuración  archivo `.env`**:

  
    ```
    API_KEY_GEMINI=api_key_de_gemini
    USUARIO_MAIL= contraseña GMAIL
    CONTRASENA_MAIL=contraseña de aplicacion  GMAIL
    ```

---

## Uso

1. Ejecuta la aplicación:

    ```bash
    python app.py
    ```

2. Abre tu navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000)

3. Ingresa tu nombre y correo electrónico, chatea con Gemini y al finalizar haz clic en el botón **Limpiar** para guardar la conversación.

4. Las conversaciones se almacenan en `chat.db` en la tabla `chat`.

---

## Estructura de la base de datos

Tabla: **chat**

| Campo           | Tipo     | Descripción                           |
|-----------------|----------|---------------------------------------|
| id              | Integer  | Clave primaria (autoincremental)      |
| usuario_nombre  | String   | Nombre del usuario                    |
| correo          | String   | Correo electrónico del usuario        |
| texto           | Text     | Conversación completa (historial chat)|


---

## Seguridad


- Las variables de entorno globales  en el archivo  `.env`  `.gitignore`.

---

## Créditos

Desarrollado por Carlos Bodero.

---

## Licencia

Este proyecto se proporciona bajo la licencia MIT. Puedes modificar y usar el código libremente.

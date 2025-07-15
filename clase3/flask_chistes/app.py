import requests
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def chiste():
    chiste = {}
    error = None

    try:
        response = requests.get("https://official-joke-api.appspot.com/jokes/random")
        if response.status_code == 200:
            chiste = response.json()
        else:
            error = "No se pudo obtener un chiste. Intenta de nuevo."
    except Exception as e:
        error = f"Error al conectarse a la API: {e}"

    return render_template("index.html", chiste=chiste, error=error)

@app.route('/salir')
def salir():
    return "<h2 style='text-align:center;margin-top:40px;'>👋 ¡Gracias por reír con nosotros! Hasta la próxima.</h2>"

if __name__ == '__main__':
    app.run(debug=True)

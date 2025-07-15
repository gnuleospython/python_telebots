from flask import Flask, render_template
import requests

app = Flask(__name__)

def obtener_chiste():
    url = "https://official-joke-api.appspot.com/jokes/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data.get("setup"), data.get("punchline")
    except requests.RequestException:
        return "Error al obtener el chiste.", ""

@app.route("/")
def index():
    setup, punchline = obtener_chiste()
    return render_template("index.html", setup=setup, punchline=punchline)

if __name__ == "__main__":
    app.run(debug=True)

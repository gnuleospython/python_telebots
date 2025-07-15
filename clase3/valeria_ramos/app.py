from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def mostrar_chiste():
    url = "https://official-joke-api.appspot.com/jokes/random"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return render_template('index.html', setup=data['setup'], punchline=data['punchline'])
    except Exception as e:
        return f"Ocurrió un error: {e}"

if __name__ == '__main__':
    app.run(debug=True)

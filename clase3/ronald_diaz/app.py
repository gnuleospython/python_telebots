from flask import Flask, render_template, request, abort
import requests

app = Flask(__name__)

"""
Ejercicio 1:Comsumo Api Pokemon
"""

API_BASE = "https://pokeapi.co/api/v2/pokemon"
PAGE_SIZE = 12

def listaPokemonesPage(page):
    offset = (page - 1) * PAGE_SIZE
    resp = requests.get(f"{API_BASE}?limit={PAGE_SIZE}&offset={offset}")
    resp.raise_for_status()
    data = resp.json()
    return data['results'], bool(data['next']), bool(data['previous'])

def obtenerPokemon(name):
    resp = requests.get(f"{API_BASE}/{name.lower()}")
    if resp.status_code == 404:
        return None
    resp.raise_for_status()
    return resp.json()

@app.route('/lista')
def listado():
    page = request.args.get('page', 1, type=int)
    pokes, has_next, has_prev = listaPokemonesPage(page)
    return render_template('listadoPokes.html', pokemons=pokes, page=page, has_next=has_next, has_prev=has_prev)


@app.route('/pokemon/<name>')
def detalle(name):
    p = obtenerPokemon(name)
    if not p:
        abort(404)
    context = {
        'id': p['id'],
        'name': p['name'].capitalize(),
        'types': [t['type']['name'] for t in p['types']],
        'abilities': [a['ability']['name'] for a in p['abilities']],
        'height': p['height'],
        'weight': p['weight'],
        'base_experience': p['base_experience'],
        'stats': {s['stat']['name']: s['base_stat'] for s in p['stats']},
        'sprite': p['sprites']['front_default'],
        'moves_count': len(p['moves'])
    }
    return render_template('detallePoke.html', **context)

"""
Ejercicio 2 Consumo Api de chistes
"""
def obtener_chiste():
    resp = requests.get('https://official-joke-api.appspot.com/jokes/random')
    resp.raise_for_status()
    return resp.json()

@app.route('/chistes')
def chistes():
    joke = obtener_chiste()
    return render_template('chiste.html', setup=joke['setup'], punchline=joke['punchline'])

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
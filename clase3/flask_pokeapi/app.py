import math

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    page = int(request.args.get('page', 1))
    search = request.args.get('search', '').lower()
    per_page = 9
    total_pokemons = 100
    offset = (page - 1) * per_page
    pokemons = []

    if search:
        data = get_pokemon(search)
        if data:
            pokemons.append(data)
        total_pages = 1
    else:
        url = f'https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={per_page}'
        response = requests.get(url)
        results = response.json().get('results', [])
        for item in results:
            poke_data = get_pokemon(item['name'])
            if poke_data:
                pokemons.append(poke_data)
        total_pages = math.ceil(total_pokemons / per_page)

    return render_template('index.html',
                           pokemon_list=pokemons,
                           search_query=search,
                           page=page,
                           total_pages=total_pages)

def get_pokemon(name):
    url = f'https://pokeapi.co/api/v2/pokemon/{name}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'name': data['name'].capitalize(),
            'image_front': data['sprites']['front_default'],
            'image_back': data['sprites']['back_default'],
            'height': data['height'],
            'weight': data['weight'],
            'abilities': [a['ability']['name'] for a in data['abilities']]
        }
    return None

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

POKEMONS_PER_PAGE = 9

@app.route('/', methods=['GET'])
def index():
    search_query = request.args.get('search', '').lower()
    page = int(request.args.get('page', 1))

    offset = (page - 1) * POKEMONS_PER_PAGE
    url = f'https://pokeapi.co/api/v2/pokemon?limit={POKEMONS_PER_PAGE}&offset={offset}'
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error al obtener los Pokémon"

    results = response.json()
    all_pokemon = []

    for poke in results['results']:
        poke_data = requests.get(poke['url']).json()
        name = poke_data['name']

        if search_query in name:
            held_items = [item['item']['name'] for item in poke_data['held_items']] if poke_data['held_items'] else ['None']
            species_name = poke_data['species']['name'] if 'species' in poke_data else 'Unknown'

            pokemon = {
            'name': name.upper(),
            'front_sprite': poke_data['sprites']['front_default'],
            'back_sprite': poke_data['sprites']['back_default'],
            'front_image': poke_data['sprites']['other']['official-artwork']['front_default'],
            'back_image': poke_data['sprites']['other']['official-artwork'].get('back_default', None),
            'height': poke_data['height'],
            'weight': poke_data['weight'],
            'moves': [move['move']['name'] for move in poke_data['moves']] if poke_data['moves'] else ['None'],
            'abilities': [a['ability']['name'] for a in poke_data['abilities']],
            'base_experience': poke_data['base_experience'],
            'order': poke_data['order'],
            'held_items': held_items,
            'types': [t['type']['name'] for t in poke_data['types']],
            'stats': {s['stat']['name']: s['base_stat'] for s in poke_data['stats']},
            'species': species_name
            }
        all_pokemon.append(pokemon)

    total = 100  
    total_pages = math.ceil(total / POKEMONS_PER_PAGE)

    return render_template('index.html', 
                           pokemon_list=all_pokemon,
                           search_query=search_query,
                           page=page,
                           total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)   

@app.route('/')
def index():
    # Diccionario para traducir los stats al español
    stats_traduccion = {
        "hp": "PS",
        "attack": "Ataque",
        "defense": "Defensa",
        "special-attack": "Ataque Especial",
        "special-defense": "Defensa Especial",
        "speed": "Velocidad"
    }

    search_query = request.args.get('search', '').lower()
    page = int(request.args.get('page', 1))
    POKEMONS_PER_PAGE = 9 
    offset = (page - 1) * POKEMONS_PER_PAGE + 20

    pokemons = []

    if search_query:
        url = f'https://pokeapi.co/api/v2/pokemon/{search_query}'
        response = requests.get(url)
        if response.status_code == 200:
            info_poke = response.json()

            species_url = info_poke['species']['url']
            species_response = requests.get(species_url)
            if species_response.status_code == 200:
                species_info = species_response.json()
                gender_rate = species_info.get('gender_rate', -1)
                if gender_rate == -1:
                    gender = "Desconocido"
                elif gender_rate == 0:
                    gender = "Solo macho"
                elif gender_rate == 8:
                    gender = "Solo hembra"
                else:
                    gender = f"Macho {100 - gender_rate * 12.5}%, Hembra {gender_rate * 12.5}%"
                habitat = species_info['habitat']['name'] if species_info['habitat'] else "Desconocido"
                color = species_info['color']['name'] if species_info['color'] else "Desconocido"
            else:
                gender = "Desconocido"
                habitat = "Desconocido"
                color = "Desconocido"

            # Traducir los stats
            stats_es = {stats_traduccion.get(s['stat']['name'], s['stat']['name']).capitalize(): s['base_stat'] for s in info_poke["stats"]}

            pokemons.append({
                'name': info_poke['name'].upper(),
                'id': info_poke['id'],
                'sprite': info_poke['sprites']['front_default'],
                'image': info_poke['sprites']['other']['official-artwork']['front_shiny'],
                'types': [t['type']['name'] for t in info_poke['types']],
                'height': info_poke['height'],
                'weight': info_poke['weight'],
                'abilities': [a['ability']['name'] for a in info_poke['abilities']],
                'stats': stats_es,
                'species': info_poke["species"]["name"].capitalize(),
                'gender': gender,
                'habitat': habitat,
                'color': color
            })
            total_pages = 1
            page = 1
    else:
        url = f'https://pokeapi.co/api/v2/pokemon?limit={POKEMONS_PER_PAGE}&offset={offset}'
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json()
            for poke in results['results']:
                detail_response = requests.get(poke['url'])
                if detail_response.status_code == 200:
                    info_poke = detail_response.json()
                    species_url = info_poke['species']['url']
                    species_response = requests.get(species_url)
                    if species_response.status_code == 200:
                        species_info = species_response.json()
                        gender_rate = species_info.get('gender_rate', -1)
                        if gender_rate == -1:
                            gender = "Desconocido"
                        elif gender_rate == 0:
                            gender = "Solo macho"
                        elif gender_rate == 8:
                            gender = "Solo hembra"
                        else:
                            gender = f"Macho {100 - gender_rate * 12.5}%, Hembra {gender_rate * 12.5}%"
                        habitat = species_info['habitat']['name'] if species_info['habitat'] else "Desconocido"
                        color = species_info['color']['name'] if species_info['color'] else "Desconocido"
                    else:
                        gender = "Desconocido"
                        habitat = "Desconocido"
                        color = "Desconocido"

                    stats_es = {stats_traduccion.get(s['stat']['name'], s['stat']['name']).capitalize(): s['base_stat'] for s in info_poke["stats"]}

                    pokemons.append({
                        'name': info_poke['name'].upper(),
                        'id': info_poke['id'],
                        'sprite': info_poke['sprites']['front_default'],
                        'image': info_poke['sprites']['other']['official-artwork']['front_shiny'],
                        'types': [t['type']['name'] for t in info_poke['types']],
                        'height': info_poke['height'],
                        'weight': info_poke['weight'],
                        'abilities': [a['ability']['name'] for a in info_poke['abilities']],
                        'stats': stats_es,
                        'species': info_poke["species"]["name"].capitalize(),
                        'gender': gender,
                        'habitat': habitat,
                        'color': color
                    })
        total = 100  
        total_pages = math.ceil((total - 20) / POKEMONS_PER_PAGE)

    return render_template('index.html', 
                           pokemon_list=pokemons,
                           search_query=search_query,
                           page=page,
                           total_pages=total_pages)

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
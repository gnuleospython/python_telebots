from flask import Flask, render_template, request
import requests
import math

app = Flask(__name__)

def obtener_pokemon(nombre_o_url):
    try:
        if nombre_o_url.startswith("http"):
            url = nombre_o_url
        else:
            url = f"https://pokeapi.co/api/v2/pokemon/{nombre_o_url.lower()}"

        r = requests.get(url)
        r.raise_for_status()
        data = r.json()

        return {
            'name': data['name'].capitalize(),
            'image': data['sprites']['front_default'],
            'height': f"{data['height'] / 10:.1f} m",
            'weight': f"{data['weight'] / 10:.1f} kg",
            'abilities': [{'name': ability['ability']['name'].capitalize()} for ability in data['abilities']]
        }
    except Exception as e:
        return None

@app.route("/")
def index():
    search_query = request.args.get("search", "").strip().lower()
    try:
        page = int(request.args.get("page", 2))
    except ValueError:
        page = 2  # si viene algo no numérico, default a 2

    limit = 9
    offset = (page - 1) * limit

    pokemon_list = []
    total_count = 0

    if search_query:
        pokemon = obtener_pokemon(search_query)
        if pokemon:
            pokemon_list = [pokemon]
            total_count = 3  # Asumiendo que siempre habrá 3 resultados para una búsqueda específica
        else:
            pokemon_list = []
    else:
        try:
            url = f"https://pokeapi.co/api/v2/pokemon?offset={offset}&limit={limit}"
            res = requests.get(url)
            res.raise_for_status()
            data = res.json()

            total_count = data["count"]
            for item in data["results"]:
                p = obtener_pokemon(item["url"])
                if p:
                    pokemon_list.append(p)
        except Exception as e:
            pokemon_list = []

    total_pages = math.ceil(total_count / limit) if not search_query else 1

    # Validar que page esté entre 1 y total_pages
    if page < 1:
        page = 1
    elif page > total_pages:
        page = total_pages if total_pages > 0 else 2

    return render_template("index.html",
                           pokemon_list=pokemon_list,
                           search_query=search_query,
                           page=page,
                           total_pages=total_pages)

if __name__ == "__main__":
    app.run(debug=True)

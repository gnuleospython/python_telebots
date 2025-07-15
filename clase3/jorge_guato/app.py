from flask import Flask, render_template, request
import requests, random

app = Flask(__name__)

# 🔍 Obtener detalle de un Pokémon desde su URL
def obtener_pokemon_detalle(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        return {
            "ID": data['id'],
            "Nombre": data['name'].capitalize(),
            "Altura": data['height'],
            "Peso": data['weight'],
            "Experiencia base": data['base_experience'],
            "Tipos": [t['type']['name'] for t in data['types']],
            "Habilidades": [h['ability']['name'] for h in data['abilities']],
            "Imagen": data['sprites']['front_default'],
            "Orden": data['order'],
            "Movimientos": [m['move']['name'] for m in data['moves'][:3]],
        }
    except Exception as e:
        print(f"❌ Error al obtener detalles: {e}")
        return None

# 📄 Obtener 9 Pokémon por página
def obtener_pokemons_por_pagina(pagina=1, por_pagina=9):
    url = f"https://pokeapi.co/api/v2/pokemon?offset={(pagina - 1) * por_pagina}&limit={por_pagina}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        data = res.json()
        pokemons = []
        for p in data['results']:
            info = obtener_pokemon_detalle(p['url'])
            if info:
                pokemons.append(info)
        return pokemons
    except Exception as e:
        print(f"❌ Error al obtener lista: {e}")
        return []

# 🎲 Obtener 3 Pokémon aleatorios
def obtener_3_pokemons_azar():
    pokemons = []
    for pid in random.sample(range(1, 1000), 3):
        info = obtener_pokemon_detalle(f"https://pokeapi.co/api/v2/pokemon/{pid}")
        if info:
            pokemons.append(info)
    return pokemons

# 😂 Obtener chiste desde JokeAPI
def obtener_chiste():
    try:
        res = requests.get("https://v2.jokeapi.dev/joke/Any?type=twopart")
        res.raise_for_status()
        data = res.json()
        return {
            "setup": data["setup"],
            "punchline": data["delivery"]
        }
    except:
        return None

# 🏠 Inicio y búsqueda de Pokémon
@app.route("/")
@app.route("/pokemon")
def buscar_pokemon():
    nombre = request.args.get("pokemon")
    pokemon = None
    if nombre:
        pokemon = obtener_pokemon_detalle(f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}")
    return render_template("index.html", pokemon=pokemon)

# 🎲 3 Pokémon aleatorios
@app.route("/random")
def mostrar_aleatorios():
    pokemons = obtener_3_pokemons_azar()
    return render_template("index.html", random_pokemons=pokemons)

# 📄 Paginación de Pokémon (página 1 por defecto)
@app.route("/menu")
def menu():
    opcion = request.args.get("opcion")
    if opcion == "pagina":
        pokemons = obtener_pokemons_por_pagina(pagina=1)
        return render_template("index.html", pokemons_pagina=pokemons)
    elif opcion == "random":
        return mostrar_aleatorios()
    return render_template("index.html")

# 😂 Chiste aleatorio
@app.route("/joke")
def chiste():
    joke = obtener_chiste()
    return render_template("index.html", joke=joke)

if __name__ == "__main__":
    app.run(debug=True)

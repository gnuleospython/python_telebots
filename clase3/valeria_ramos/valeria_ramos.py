import requests


limit = 9
offset = 0

while True:
    url = f"https://pokeapi.co/api/v2/pokemon?limit={limit}&offset={offset}"
    response = requests.get (url)
    
    if response.status_code == 200:
        data = response.json()
        print (f"Mostrando Pokemmón {offset+1} a {offset+limit}")
        for poke in data ['results']:
            print ("-", poke['name'])
    else: 
        print ("Error al obtener datos.")
        break
    option = input ("Ver más.. (s/n):")
    if option.lower() == 's':
        offset += limit
    else:
        break
nombre = input ("\n Ingresa el nombre del Pokemón para ver sus datos:")

url_pokemon = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
resp_poke = requests.get(url_pokemon)

if resp_poke.status_code == 200:
    datos = resp_poke.json()
    print("\nDatos del Pokémon:")
    print("ID:", datos['id'])
    print("Nombre:", datos['name'])
    tipos = [t['type']['name'] for t in datos['types']]
    print("Tipos:", tipos)
    print("Altura:", datos['height'])
    print("Imagen URL:", datos['sprites']['front_default'])
    print("Sprite:", datos['sprites']['front_default'])
else:
    print("Pokémon no encontrado.")
    
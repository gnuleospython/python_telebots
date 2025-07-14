import requests

def traducir_mymemory(texto, origen='en', destino='es'):
    url = 'https://api.mymemory.translated.net/get'
    params = {
        'q': texto,
        'langpair': f'{origen}|{destino}'
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['responseData']['translatedText']
        else:
            print('❌ Error al traducir (API MyMemory).')
            return texto
    except requests.RequestException as e:
        print(f'⚠️ Error de conexión al traducir: {e}')
        return texto

def chiste():
    try:
        response = requests.get('https://official-joke-api.appspot.com/random_joke')
        if response.status_code == 200:
            data = response.json()
            setup_en = data['setup']
            punchline_en = data['punchline']
            setup_es = traducir_mymemory(setup_en)
            punchline_es = traducir_mymemory(punchline_en)
            return setup_es, punchline_es
        else:
            print('❌ No se pudo obtener un chiste (Error en la API).')
            return None, None
    except requests.RequestException as e:
        print(f'⚠️ Error de conexión: {e}')
        return None, None

def pedir_entrada(prompt):
    entrada = input(prompt)
    return entrada.strip().lower()

def main():
    print('🤣 Presiona ENTER para ver un chiste o escribe SALIR para terminar.\n')

    entrada = pedir_entrada('')
    if entrada == 'salir':
        print('\n💥 ¡El programa terminó… pero el humor sigue disponible!\n')
        return

    while True:
        setup, punchline = chiste()
        if setup and punchline:
            print(f'\n🗯️  {setup}')
            print(f'😂  {punchline}\n')
        else:
            print('😅 Intenté traer un chiste, pero se fue corriendo del susto xd.')

        entrada = pedir_entrada('¿Quieres OTRO chiste? (ENTER para sí / SALIR para no): ')
        if entrada == 'salir':
            print('\n💥 ¡El programa terminó… pero el humor sigue disponible!\n')
            break

if __name__ == "__main__":
    main()

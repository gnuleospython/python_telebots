import json

import requests

URL = "https://fakestoreapi.com"

def deserialize_json(json_data):
    """
    Deserialize JSON data into a Python object.
    """
    try:
        return json_data.json()
    except ValueError as e:
        print(f"Error deserializing JSON: {e}")
        return None
    
def serialize_json(data):
    """
    Serialize a Python object into JSON format.
    """
    try:
        return json.dumps(data, indent=2)
    except TypeError as e:
        print(f"Error serializing to JSON: {e}")
        return None

def get_products():
    url = f"{URL}/products"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_product_by_id(product_id):
    url = f"{URL}/products/{product_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

if __name__ == "__main__":
    products = get_products()
    for product in products:
        print(f"Product ID: {product['id']}")
        print(f"Title: {product['title']}")
        print(f"Price: {product['price']}")
        print(f"Description: {product['description']}")
        print(f"Imagen: {product['image']}")
        print("-" * 20)
        
    product = get_product_by_id(15)
    print(f"Product ID: {product['id']}")
    print(f"Title: {product['title']}")
    print(f"Price: {product['price']}")
    print(f"Description: {product['description']}")
    print(f"Imagen: {product['image']}")
    print("-" * 20)
    
    objserialize = serialize_json(products)
    print(f"Serialized JSON: {objserialize}")
    
    # objDeserialize = deserialize_json(response)
    # print(f"Deserialized JSON: {objDeserialize}")


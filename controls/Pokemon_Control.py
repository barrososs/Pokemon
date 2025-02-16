from flask import Blueprint, jsonify
import requests
import random
from resources.Config import Config
from flask_jwt_extended import jwt_required, get_jwt_identity

pokemon_bp = Blueprint("pokemon_bp", __name__)

@pokemon_bp.route('/detalle/<pokemon_name>', methods=['GET'])
@jwt_required()
def get_pokemon_detail(pokemon_name: str):
    current_user = get_jwt_identity()
    try:
        url = f"{Config.POKEAPI_URL}pokemon/{pokemon_name.lower()}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as error:
        return jsonify({"msg": f"Error al consultar la PokeAPI: {error}"}), 500
    pokemon_data = response.json()
    resultado = {
        "nombre": pokemon_data['name'],
        "tipos": [tipo['type']['name'] for tipo in pokemon_data['types']],
        "habilidades": [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']],
        "estadisticas": {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']},
        "movimientos": [movimiento['move']['name'] for movimiento in pokemon_data['moves']],
        "usuario": current_user
    }
    return jsonify(resultado), 200

@pokemon_bp.route('/aleatorio/<tipo>', methods=['GET'])
@jwt_required()
def get_random_pokemon_by_type(tipo: str):
    current_user = get_jwt_identity()
    try:
        url = f"{Config.POKEAPI_URL}type/{tipo.lower()}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as error:
        return jsonify({"msg": f"Error al consultar el tipo en PokeAPI: {error}"}), 500
    data = response.json()
    pokemons = data.get("pokemon", [])
    if not pokemons:
        return jsonify({"msg": "No se encontraron Pokémon para este tipo"}), 404
    pokemon_aleatorio = random.choice(pokemons)["pokemon"]
    pokemon_url = pokemon_aleatorio["url"]
    try:
        pokemon_response = requests.get(pokemon_url)
        pokemon_response.raise_for_status()
    except requests.RequestException as error:
        return jsonify({"msg": f"Error al obtener detalles del Pokémon: {error}"}), 500
    pokemon_data = pokemon_response.json()
    resultado = {
        "nombre": pokemon_data['name'],
        "tipos": [tipo_data['type']['name'] for tipo_data in pokemon_data['types']],
        "habilidades": [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']],
        "estadisticas": {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']},
        "movimientos": [movimiento['move']['name'] for movimiento in pokemon_data['moves']],
        "usuario": current_user
    }
    return jsonify(resultado), 200

@pokemon_bp.route('/maslargo/<tipo>', methods=['GET'])
@jwt_required()
def get_longest_name_pokemon_by_type(tipo: str):
    current_user = get_jwt_identity()
    try:
        url = f"{Config.POKEAPI_URL}type/{tipo.lower()}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as error:
        return jsonify({"msg": f"Error al consultar el tipo en PokeAPI: {error}"}), 500
    data = response.json()
    pokemons = data.get("pokemon", [])
    if not pokemons:
        return jsonify({"msg": "No se encontraron Pokémon para este tipo"}), 404
    longest_pokemon = max(pokemons, key=lambda p: len(p["pokemon"]["name"]))["pokemon"]
    pokemon_url = longest_pokemon["url"]
    try:
        pokemon_response = requests.get(pokemon_url)
        pokemon_response.raise_for_status()
    except requests.RequestException as error:
        return jsonify({"msg": f"Error al obtener detalles del Pokémon: {error}"}), 500
    pokemon_data = pokemon_response.json()
    resultado = {
        "nombre": pokemon_data['name'],
        "tipos": [tipo_data['type']['name'] for tipo_data in pokemon_data['types']],
        "habilidades": [habilidad['ability']['name'] for habilidad in pokemon_data['abilities']],
        "estadisticas": {stat['stat']['name']: stat['base_stat'] for stat in pokemon_data['stats']},
        "movimientos": [movimiento['move']['name'] for movimiento in pokemon_data['moves']],
        "usuario": current_user
    }
    return jsonify(resultado), 200

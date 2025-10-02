import requests
import json

# URL donde está corriendo tu servidor. Si es en el mismo PC, esta es la correcta.
SERVER_URL = "http://192.168.1.50:5000"

def cargar_puntajes_online():
    """Obtiene los mejores puntajes desde el servidor."""
    try:
        response = requests.get(f"{SERVER_URL}/get_scores")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con el servidor: {e}")
        return []

def registrar_puntaje_online(nombre, puntaje):
    """Envía un nuevo puntaje al servidor."""
    payload = {"player_name": nombre, "score": int(puntaje)}
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(f"{SERVER_URL}/add_score", data=json.dumps(payload), headers=headers)
        response.raise_for_status()
        print("Puntaje enviado exitosamente.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al enviar el puntaje: {e}")
        return False

def obtener_record_online():
    """Obtiene el puntaje más alto de todos para mostrarlo como récord."""
    puntajes = cargar_puntajes_online()
    if puntajes:
        return puntajes[0].get('max_score', 0)
    return 0
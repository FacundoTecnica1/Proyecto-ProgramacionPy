from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

# --- CONFIGURACIÓN ---
# REEMPLAZA ESTO CON TUS CREDENCIALES DE MYSQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'RedesInformaticas',
    'database': 'Dinosaurio'
}

app = Flask(__name__)
CORS(app) # Permite que tu juego se conecte al servidor

def get_db_connection():
    """Crea y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error de conexión a la base de datos: {err}")
        return None

@app.route('/get_scores', methods=['GET'])
def get_scores():
    """Devuelve los 10 mejores puntajes únicos por jugador."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
    
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT player_name, MAX(score) as max_score
        FROM high_scores
        GROUP BY player_name
        ORDER BY max_score DESC
        LIMIT 10;
    """
    
    cursor.execute(query)
    scores = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(scores)

@app.route('/add_score', methods=['POST'])
def add_score():
    """Añade un nuevo puntaje a la base de datos."""
    data = request.json
    player_name = data.get('player_name')
    score = data.get('score')

    if not player_name or score is None:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500
        
    cursor = conn.cursor()
    query = "INSERT INTO high_scores (player_name, score) VALUES (%s, %s)"
    cursor.execute(query, (player_name, score))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": "Puntaje agregado"}), 201

if __name__ == '__main__':
    # Inicia el servidor. Debe estar corriendo para que el juego funcione.
    app.run(host='0.0.0.0', port=5000)
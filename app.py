from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Adiciona a configuração do CORS

# Criação da base de dados
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Base de dados aberta com sucesso")
    conn.execute('CREATE TABLE IF NOT EXISTS cotacao (id INTEGER PRIMARY KEY, name TEXT, email TEXT, phone TEXT, description TEXT)')
    print("Tabela criada com sucesso")
    conn.close()

init_sqlite_db()

@app.route('/')
def home():
    return render_template('index.html')  # Aqui estamos retornando a página inicial (index.html)

@app.route('/api/cotacao', methods=['POST'])
def criar_cotacao():
    try:
        data = request.get_json()
        
        # Validações básicas
        if not all(key in data for key in ['name', 'email', 'phone', 'description']):
            return jsonify({"error": "Faltam campos obrigatórios"}), 400

        name = data['name'].upper()
        email = data['email'].lower()
        phone = data['phone']
        description = data['description'].upper()
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO cotacao (name, email, phone, description)
                           VALUES (?, ?, ?, ?)""", (name, email, phone, description))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"message": "Orçamento solicitado com sucesso!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/cotacoes', methods=['GET'])
def listar_cotacoes():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cotacao")
        rows = cursor.fetchall()

        # Estruturação dos dados como uma lista de dicionários
        cotacoes = [
            {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "description": row[4]}
            for row in rows
        ]

        cursor.close()
        conn.close()

        return jsonify(cotacoes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/cotacoes')
def cotacoes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cotacao")
    cotacoes = cursor.fetchall()
    conn.close()
    
    return render_template('cotacoes.html', cotacoes=cotacoes)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Aqui, 5000 é o valor default
    app.run(host="0.0.0.0", port=port)

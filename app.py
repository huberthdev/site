from flask import Flask, request, redirect, jsonify, render_template
from flask_cors import CORS
import sqlite3
import os
import logging

# Configuração de logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "https://www.servhidel.com.br"}})  # Restrição de CORS

@app.before_request
def handle_redirects():
    """Redireciona para www e força HTTPS."""
    # Redireciona para www.servhidel.com.br
    if request.host == 'servhidel.com.br':
        return redirect('https://www.servhidel.com.br' + request.full_path, code=301)
    
    # Garante HTTPS
    if not request.is_secure and 'HEROKU' in os.environ:
        return redirect(request.url.replace("http://", "https://"), code=301)


# Função para inicializar o banco de dados SQLite
def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    logging.info("Base de dados aberta com sucesso")
    conn.execute('''CREATE TABLE IF NOT EXISTS cotacao (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        description TEXT NOT NULL
    )''')
    logging.info("Tabela criada ou já existente")
    conn.close()

# Inicializa o banco de dados ao iniciar o servidor
init_sqlite_db()

@app.route('/')
def home():
    """Rota para a página inicial."""
    return render_template('index.html')

@app.route('/api/cotacao', methods=['POST'])
def criar_cotacao():
    """Rota para criar uma nova cotação."""
    try:
        data = request.get_json()

        # Validações básicas
        if not all(key in data for key in ['name', 'email', 'phone', 'description']):
            return jsonify({"error": "Faltam campos obrigatórios"}), 400

        name = data['name'].upper()
        email = data['email'].lower()
        phone = data['phone']
        description = data['description'].upper()

        # Conexão com o banco de dados
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO cotacao (name, email, phone, description)
                           VALUES (?, ?, ?, ?)""", (name, email, phone, description))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Orçamento solicitado com sucesso!\n\nEntraremos em contato em breve."}), 201
    except sqlite3.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({"error": "Erro no banco de dados"}), 500
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cotacoes', methods=['GET'])
def listar_cotacoes():
    """Rota para listar todas as cotações."""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cotacao")
        rows = cursor.fetchall()

        cotacoes = [
            {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "description": row[4]}
            for row in rows
        ]

        cursor.close()
        conn.close()

        return jsonify(cotacoes), 200
    except sqlite3.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({"error": "Erro no banco de dados"}), 500
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/cotacoes')
def cotacoes():
    """Rota para renderizar a página de cotações."""
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cotacao")
        cotacoes = cursor.fetchall()
        conn.close()

        return render_template('cotacoes.html', cotacoes=cotacoes)
    except sqlite3.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        return render_template('error.html', error="Erro ao acessar o banco de dados")
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Porta padrão para Heroku
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, redirect, jsonify, render_template, session, flash
from flask_cors import CORS
import psycopg2
import os
import logging
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração de logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessao"  # Para sessões
CORS(app, resources={r"/api/*": {"origins": "https://www.servhidel.com.br"}})  # Restrição de CORS

# Configurações do PostgreSQL
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', 5432)  # Porta padrão 5432
}

def get_db_connection():
    """Estabelece uma conexão com o banco PostgreSQL."""
    return psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )

def init_db():
    """Inicializa o banco de dados, criando tabelas se necessário."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Criação da tabela de cotações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cotacao (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                phone VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                status INTEGER
            );
        """)

        # Criação da tabela de clientes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cliente (
                id_cliente SERIAL PRIMARY KEY,
                endereco TEXT,
                cep VARCHAR(10),
                cidade VARCHAR(255),
                uf VARCHAR(2),
                cpf VARCHAR(14),
                observacoes TEXT,
                id_cotacao INTEGER,
                FOREIGN KEY (id_cotacao) REFERENCES cotacao(id)
            );
        """)

        # Criação da tabela de usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id SERIAL PRIMARY KEY,
                usuario VARCHAR(255) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL,
                nivel INTEGER NOT NULL
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()
    except psycopg2.Error as e:
        logging.error(f"Erro ao inicializar o banco de dados: {e}")

@app.before_request
def handle_redirects():
    """Redireciona para www e força HTTPS."""
    if request.host == 'servhidel.com.br':
        return redirect('https://www.servhidel.com.br' + request.full_path, code=301)
    if not request.is_secure and 'HEROKU' in os.environ:
        return redirect(request.url.replace("http://", "https://"), code=301)

# Página inicial
@app.route('/')
def home():
    return render_template('index.html')

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Consulta para validar a combinação de usuário e senha
            cursor.execute("SELECT id, nivel, usuario FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['nivel'] = user[1]

                # Extrai o primeiro nome antes do ponto e formata com a primeira letra maiúscula
                primeiro_nome = user[2].split('.')[0].capitalize()
                session['username'] = primeiro_nome  # Salva o nome formatado na sessão

                # Redireciona com base no nível de acesso
                if user[1] == 1:  # Administrador
                    return redirect('/')
                elif user[1] == 2:  # Usuário
                    return redirect('/')
                else:
                    flash("Nível de acesso inválido.", "error")
                    return redirect('/login')
            else:
                flash("Usuário ou senha incorretos.", "error")

        except psycopg2.Error as e:
            logging.error(f"Erro no banco de dados: {e}")
            flash("Erro no banco de dados. Tente novamente mais tarde.", "error")
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

# Página do usuário
@app.route('/meuorcamento')
def meuorcamento():
    if session.get('nivel') == 2:
        return render_template('meuorcamento.html')
    return redirect('/login')

@app.route('/cotacoes')
def cotacoes():
    if 'user_id' not in session:
        flash("Você precisa estar logado para acessar esta página.", "error")
        return redirect('/login')
    
    if session.get('nivel') != 1:
        flash("Você não tem permissão para acessar esta página.", "error")
        return redirect('/')

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta ao banco de dados
        cursor.execute("SELECT * FROM cotacao")
        cotacoes = cursor.fetchall()

        # Fechar conexão
        cursor.close()
        conn.close()

        # Renderizar os dados
        return render_template('cotacoes.html', cotacoes=cotacoes)
    except psycopg2.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        flash("Erro ao buscar os dados do banco de dados.", "error")
        return render_template('error.html', error="Erro ao acessar os dados.")
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        flash("Erro inesperado ao buscar os dados.", "error")
        return render_template('error.html', error=str(e))

@app.route('/api/cotacao', methods=['POST'])
def criar_cotacao():
    try:
        data = request.get_json()
        if not all(key in data for key in ['name', 'email', 'phone', 'description']):
            return jsonify({"error": "Faltam campos obrigatórios"}), 400

        name = data['name'].upper()
        email = data['email'].lower()
        phone = data['phone']
        description = data['description'].upper()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cotacao (name, email, phone, description, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, description, 0))  # Assume o status como 0 por padrão
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Orçamento solicitado com sucesso!\n\nEntraremos em contato em breve."}), 201
    except psycopg2.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({"error": "Erro no banco de dados"}), 500
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/cotacoes', methods=['GET'])
def listar_cotacoes():
    try:
        # Pega os parâmetros de página e número de itens por página
        page = int(request.args.get('page', 1))  # Página padrão 1
        per_page = int(request.args.get('per_page', 10))  # Itens por página padrão 10
        
        offset = (page - 1) * per_page  # Calcula o offset para a consulta

        conn = get_db_connection()
        cursor = conn.cursor()

        # Consulta para pegar as cotações com paginação
        cursor.execute(f"""
            SELECT * FROM cotacao
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        rows = cursor.fetchall()

        # Consulta para pegar o número total de cotações
        cursor.execute("SELECT COUNT(*) FROM cotacao")
        total = cursor.fetchone()[0]

        cotacoes = [
            {"id": row[0], "name": row[1], "email": row[2], "phone": row[3], "description": row[4], "status": row[5]}
            for row in rows
        ]

        cursor.close()
        conn.close()

        return jsonify({"cotacoes": cotacoes, "total": total}), 200
    except psycopg2.Error as e:
        logging.error(f"Erro no banco de dados: {e}")
        return jsonify({"error": "Erro no banco de dados"}), 500
    except Exception as e:
        logging.error(f"Erro geral: {e}")
        return jsonify({"error": str(e)}), 500

# Adicione o nome do usuário nos templates
@app.context_processor
def inject_user():
    return {'username': session.get('username', '')}

@app.route('/admin', methods=['GET'])
def admin():
    if session.get('nivel') == 1:
        return render_template('admin.html')
    return redirect('/login')

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

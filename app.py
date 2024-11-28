from flask import Flask, request, redirect, jsonify, render_template, session, flash
from flask_cors import CORS
from dotenv import load_dotenv
import psycopg2, os, logging


load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = "chave_secreta_para_sessao"
CORS(app, resources={r"/api/*": {"origins": "https://www.servhidel.com.br"}})

# Configurações do PostgreSQL
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', 5432)
}

def get_db_connection():
    """Faz a conexão com o banco PostgreSQL."""
    return psycopg2.connect(
        dbname=DB_CONFIG['dbname'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port']
    )

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        senha = request.form.get('senha')

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT id, nivel, nome FROM usuarios WHERE usuario = %s AND senha = %s", (usuario, senha))
            user = cursor.fetchone()

            if user:
                session['user_id'] = user[0]
                session['nivel'] = user[1]
                session['username'] = user[2]

                if user[1] == 1:  # Administrador
                    return redirect('/')
                elif user[1] == 2:  # Cliente
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

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/meuprojeto')
def meuprojeto():
    if session.get('nivel') == 2:
        return render_template('meuprojeto.html')
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
        cursor.execute("SELECT * FROM cotacao")

        cotacoes = cursor.fetchall()

        cursor.close()
        conn.close()

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

        name = data['name'].upper().strip()
        email = data['email'].lower().strip()
        phone = data['phone'].strip()
        description = data['description'].upper().strip()

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cotacao (name, email, phone, description, status)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, description, 0))
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
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT * FROM cotacao
            ORDER BY id DESC
            LIMIT %s OFFSET %s
        """, (per_page, offset))
        rows = cursor.fetchall()

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

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if session.get('nivel') != 1:
        return redirect('/login')

    search = request.args.get('search', '')  
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT a.id_cliente as ID, b.name as NOME, a.cpf as CPF, a.observacoes as OBSERVAÇÃO
    FROM cliente a
    INNER JOIN cotacao b ON a.id_cotacao = b.id
    WHERE a.cpf ILIKE %s OR b.name ILIKE %s AND b.status < 7;
    """
    cursor.execute(query, (f'%{search}%', f'%{search}%'))
    clientes = cursor.fetchall()
    colunas = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    return render_template('admin.html', clientes=clientes, colunas=colunas)

@app.route('/excluir/<int:id_cliente>', methods=['POST'])
def excluir_cliente(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_cotacao FROM cliente WHERE id_cliente = %s", (id_cliente,))
        id_cotacao = cursor.fetchone()
        
        if id_cotacao:
            id_cotacao = id_cotacao[0]

            cursor.execute("DELETE FROM cliente WHERE id_cliente = %s", (id_cliente,))
            cursor.execute("DELETE FROM cotacao WHERE id = %s", (id_cotacao,))

        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao excluir cliente: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/admin')

@app.route('/_projeto/<int:id_cliente>', methods=['GET', 'POST'])
def _projeto(id_cliente):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Consulta para buscar os dados do cliente
    cursor.execute("""
        SELECT 
            a.id_cliente, a.id_cotacao, b.name, b.email, b.phone, b.description, c.descricao AS status, 
            a.endereco, a.cep, a.cidade, a.uf, a.observacoes, a.data_cadastro
        FROM cliente a
        INNER JOIN cotacao b ON a.id_cotacao = b.id
        INNER JOIN status c ON b.status = c.status
        WHERE a.id_cliente = %s
    """, (id_cliente,))
    cliente = cursor.fetchone()

    # Consulta para buscar as opções de status
    cursor.execute("SELECT status, descricao FROM status ORDER BY status")
    status_opcoes = cursor.fetchall()  # Retorna uma lista de tuplas (status, descricao)

    cursor.close()
    conn.close()

    if cliente:
        # Definir as colunas para o template
        colunas = [
            'id_cliente', 'id_cotacao', 'name', 'email', 'phone', 'description', 'status', 
            'endereco', 'cep', 'cidade', 'uf', 'observacoes', 'data_cadastro'
        ]
        return render_template(
            'cliente.html', 
            cliente=cliente, 
            colunas=colunas, 
            status_opcoes=status_opcoes,  # Enviar opções de status para o template
            status_atual=cliente[6],  # Passar o status atual do cliente
            id_cliente=id_cliente
        )
    else:
        return "Cliente não encontrado", 404


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

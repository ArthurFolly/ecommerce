from flask import Flask, request, jsonify, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
app.secret_key = 'SUA_CHAVE_SECRETA_AQUI'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:FOLLY07@localhost/ecommerce'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo do usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Modelo do produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(500))
    preco = db.Column(db.Float, nullable=False)
    plataforma = db.Column(db.String(50))
    categoria = db.Column(db.String(50))
    imagem = db.Column(db.String(300))
    estoque = db.Column(db.Integer, default=0)

with app.app_context():
    db.create_all()

# Rotas de autenticação
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    novo_usuario = Usuario(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'mensagem': 'Usuário registrado com sucesso!'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Usuario.query.filter_by(email=data['email']).first()

    if not user or not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({'erro': 'Credenciais inválidas.'}), 401

    session['user_id'] = user.id
    session['user_email'] = user.email
    
    return jsonify({'mensagem': 'Login realizado com sucesso!'}), 200

# Rotas de produtos
@app.route('/produtos', methods=['GET'])
def get_produtos():
    produtos = Produto.query.all()
    return jsonify([{
        'id': p.id,
        'nome': p.nome,
        'descricao': p.descricao,
        'preco': p.preco,
        'plataforma': p.plataforma,
        'categoria': p.categoria,
        'imagem': p.imagem,
        'estoque': p.estoque
    } for p in produtos]), 200

# Rotas de páginas
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET'])
def cadastro_page():
    return render_template('cadastro.html')

@app.route('/loja')
def loja():
    return render_template('loja.html')

if __name__ == '__main__':
    app.run(debug=True)
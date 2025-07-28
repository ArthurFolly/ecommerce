import pytest
from app import app, db, Usuario, Produto

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_cadastro_usuario(client):
    resposta = client.post('/register', json={
        'username': 'teste',
        'email': 'teste@email.com',
        'password': 'senha123'
    })
    assert resposta.status_code == 201

def test_login(client):
    client.post('/register', json={
        'username': 'teste',
        'email': 'teste@email.com', 
        'password': 'senha123'
    })
    resposta = client.post('/login', json={
        'email': 'teste@email.com',
        'password': 'senha123'
    })
    assert resposta.status_code == 200

def test_produtos(client):
    resposta = client.get('/produtos')
    assert resposta.status_code == 200
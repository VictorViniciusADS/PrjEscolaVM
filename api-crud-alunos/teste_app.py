import pytest
from alunos import app, db, Aluno  # Importa sua aplicação e modelos

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'SQLAlchemy'
    client = app.test_client()

    with app.app_context():
        db.create_all()
    yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_cadastrar_aluno(client):
    # Testa o cadastro de um novo aluno
    response = client.post('/alunos', json={
        "aluno_id": 1,
        "nome": "João Silva",
        "endereco": "Rua A",
        "cidade": "São Paulo",
        "estado": "SP",
        "cep": "01234-567",
        "pais": "Brasil",
        "telefone": "123456789"
    })
    assert response.status_code == 201
    assert response.json['message'] == "Aluno cadastrado com sucesso!"

def test_listar_alunos(client):
    # Testa a listagem de alunos
    client.post('/alunos', json={"aluno_id": 1, "nome": "João Silva"})
    response = client.get('/alunos')
    assert response.status_code == 200
    assert len(response.json) == 1
    assert response.json[0]['nome'] == "João Silva"

def test_alterar_aluno(client):
    # Testa a alteração de dados de um aluno
    client.post('/alunos', json={"aluno_id": 1, "nome": "João Silva"})
    response = client.put('/alunos/1', json={"nome": "João Santos"})
    assert response.status_code == 200
    assert response.json['message'] == "Dados do aluno atualizados com sucesso!"
    
    # Confirma se o nome foi alterado
    response = client.get('/alunos')
    assert response.json[0]['nome'] == "João Santos"

def test_excluir_aluno(client):
    # Testa a exclusão de um aluno
    client.post('/alunos', json={"aluno_id": 1, "nome": "João Silva"})
    response = client.delete('/alunos/1')
    assert response.status_code == 200
    assert response.json['message'] == "Aluno excluído com sucesso!"
    
    # Confirma se o aluno foi excluído
    response = client.get('/alunos')
    assert len(response.json) == 0



    
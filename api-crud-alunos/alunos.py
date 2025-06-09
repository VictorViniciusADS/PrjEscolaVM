# filepath: c:\Users\victo\OneDrive\Desktop\Aula-24-03\app.py
from flask import Flask 
from models import db, Aluno

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'  # Banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()  # Cria a tabela no banco de dados

from flask import Flask, request, jsonify
from models import db, Aluno


# Listar Alunos Cadastrados (READ)
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    alunos = Aluno.query.all()
    return jsonify([{
        "id_aluno": aluno.id_aluno,
        "nome_completo": aluno.nome_completo,
        "data_nascimento": aluno.data_nascimento.strftime('%Y-%m-%d'),
        "id_turma": aluno.id_turma,
        "nome_responsavel": aluno.nome_responsavel,
        "telefone_responsavel": aluno.telefone_responsavel,
        "email_responsavel": aluno.email_responsavel,
        "informacoes_adicionais": aluno.informacoes_adicionais
    } for aluno in alunos])

# Cadastrar Novos Alunos (CREATE)
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    data = request.json
    novo_aluno = Aluno(
        nome_completo=data['nome_completo'],
        data_nascimento=data['data_nascimento'],
        id_turma=data['id_turma'],
        nome_responsavel=data['nome_responsavel'],
        telefone_responsavel=data['telefone_responsavel'],
        email_responsavel=data['email_responsavel'],
        informacoes_adicionais=data.get('informacoes_adicionais')
    )
    db.session.add(novo_aluno)
    db.session.commit()
    return jsonify({"message": "Aluno cadastrado com sucesso!"}), 201

# Alterar Dados de Alunos Cadastrados (UPDATE)
@app.route('/alunos/<aluno_id>', methods=['PUT'])
def alterar_aluno(aluno_id):
    aluno = Aluno.query.filter_by(aluno_id=aluno_id).first()
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404

    data = request.json
    aluno.nome_completo = data.get('nome_completo', aluno.nome_completo)
    aluno.data_nascimento = data.get('data_nascimento', aluno.data_nascimento)
    aluno.id_turma = data.get('id_turma', aluno.id_turma)
    aluno.nome_responsavel = data.get('nome_responsavel', aluno.nome_responsavel)
    aluno.telefone_responsavel = data.get('telefone_responsavel', aluno.telefone_responsavel)
    aluno.email_responsavel = data.get('email_responsavel', aluno.email_responsavel)
    aluno.informacoes_adicionais = data.get('informacoes_adicionais', aluno.informacoes_adicionais)

    db.session.commit()
    return jsonify({"message": "Dados do aluno atualizados com sucesso!"})

# Excluir Alunos (DELETE)
@app.route('/alunos/<aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    aluno = Aluno.query.filter_by(aluno_id=aluno_id).first()
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno excluído com sucesso!"})
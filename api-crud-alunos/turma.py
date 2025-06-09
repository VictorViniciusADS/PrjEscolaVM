#Para executar os testes turma 

from flask import Flask, request, jsonify
from models import db, Turma

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Substitua pelo banco usado
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Modelo Turma
class Turma(db.Model):
    __tablename__ = 'turma'
    id_turma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_turma = db.Column(db.String(100), nullable=False)
    id_professor = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.String(50), nullable=False)

# Rota para listar todas as turmas
@app.route('/turmas', methods=['GET'])
def listar_turmas():
    turmas = Turma.query.all()
    return jsonify([{
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    } for turma in turmas])

# Rota para criar uma nova turma
@app.route('/turmas', methods=['POST'])
def criar_turma():
    dados = request.json
    nova_turma = Turma(
        nome_turma=dados['nome_turma'],
        id_professor=dados['id_professor'],
        horario=dados['horario']
    )
    db.session.add(nova_turma)
    db.session.commit()
    return jsonify({'message': 'Turma criada com sucesso!'}), 201

# Rota para atualizar uma turma
@app.route('/turmas/<int:id_turma>', methods=['PUT'])
def atualizar_turma(id_turma):
    turma = Turma.query.get_or_404(id_turma)
    dados = request.json
    turma.nome_turma = dados['nome_turma']
    turma.id_professor = dados['id_professor']
    turma.horario = dados['horario']
    db.session.commit()
    return jsonify({'message': 'Turma atualizada com sucesso!'})

# Rota para deletar uma turma
@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
def deletar_turma(id_turma):
    turma = Turma.query.get_or_404(id_turma)
    db.session.delete(turma)
    db.session.commit()
    return jsonify({'message': 'Turma deletada com sucesso!'})
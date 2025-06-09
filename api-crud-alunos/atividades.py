# Inicializar o banco de dados
with app.app_context():
     db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from models import db, Atividade
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Modelo Atividade
class Atividade(db.Model):
    __tablename__ = 'atividade'
    id_atividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)

# Rota para listar todas as atividades
@app.route('/atividades', methods=['GET'])
def listar_atividades():
    atividades = Atividade.query.all()
    return jsonify([{
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': str(atividade.data_realizacao)
    } for atividade in atividades])

# Rota para criar uma nova atividade
@app.route('/atividades', methods=['POST'])
def criar_atividade():
    dados = request.json
    nova_atividade = Atividade(
        descricao=dados['descricao'],
        data_realizacao=dados['data_realizacao']
    )
    db.session.add(nova_atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade criada com sucesso!'}), 201

# Rota para atualizar uma atividade
@app.route('/atividades/<int:id_atividade>', methods=['PUT'])
def atualizar_atividade(id_atividade):
    atividade = Atividade.query.get_or_404(id_atividade)
    dados = request.json
    atividade.descricao = dados['descricao']
    atividade.data_realizacao = dados['data_realizacao']
    db.session.commit()
    return jsonify({'message': 'Atividade atualizada com sucesso!'})

# Rota para deletar uma atividade
@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def deletar_atividade(id_atividade):
    atividade = Atividade.query.get_or_404(id_atividade)
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade deletada com sucesso!'})
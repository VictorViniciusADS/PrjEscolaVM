# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    #Crude para os alunos 
from flask import Flask, request, jsonify
from models import db, Presenca

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Modelo Presenca
class Presenca(db.Model):
    __tablename__ = 'presenca'
    id_presenca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, nullable=False)
    data_presenca = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

# Rota para listar todas as presenças
@app.route('/presencas', methods=['GET'])
def listar_presencas():
    presencas = Presenca.query.all()
    return jsonify([{
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': str(presenca.data_presenca),
        'presente': presenca.presente
    } for presenca in presencas])

# Rota para criar uma nova presença
@app.route('/presencas', methods=['POST'])
def criar_presenca():
    dados = request.json
    nova_presenca = Presenca(
        id_aluno=dados['id_aluno'],
        data_presenca=dados['data_presenca'],
        presente=dados['presente']
    )
    db.session.add(nova_presenca)
    db.session.commit()
    return jsonify({'message': 'Presença criada com sucesso!'}), 201

# Rota para atualizar uma presença
@app.route('/presencas/<int:id_presenca>', methods=['PUT'])
def atualizar_presenca(id_presenca):
    presenca = Presenca.query.get_or_404(id_presenca)
    dados = request.json
    presenca.id_aluno = dados['id_aluno']
    presenca.data_presenca = dados['data_presenca']
    presenca.presente = dados['presente']
    db.session.commit()
    return jsonify({'message': 'Presença atualizada com sucesso!'})

# Rota para deletar uma presença
@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
def deletar_presenca(id_presenca):
    presenca = Presenca.query.get_or_404(id_presenca)
    db.session.delete(presenca)
    db.session.commit()
    return jsonify({'message': 'Presença deletada com sucesso!'})
# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    #Para a tabela professor
from flask import Flask, request, jsonify
from models import db, Professor

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Modelo Professor
class Professor(db.Model):
    __tablename__ = 'professor'
    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)

# Rota para listar todos os professores
@app.route('/professores', methods=['GET'])
def listar_professores():
    professores = Professor.query.all()
    return jsonify([{
        'id_professor': professor.id_professor,
        'nome_completo': professor.nome_completo,
        'email': professor.email,
        'telefone': professor.telefone
    } for professor in professores])

# Rota para criar um novo professor
@app.route('/professores', methods=['POST'])
def criar_professor():
    dados = request.json
    novo_professor = Professor(
        nome_completo=dados['nome_completo'],
        email=dados['email'],
        telefone=dados['telefone']
    )
    db.session.add(novo_professor)
    db.session.commit()
    return jsonify({'message': 'Professor criado com sucesso!'}), 201

# Rota para atualizar um professor
@app.route('/professores/<int:id_professor>', methods=['PUT'])
def atualizar_professor(id_professor):
    professor = Professor.query.get_or_404(id_professor)
    dados = request.json
    professor.nome_completo = dados['nome_completo']
    professor.email = dados['email']
    professor.telefone = dados['telefone']
    db.session.commit()
    return jsonify({'message': 'Professor atualizado com sucesso!'})

# Rota para deletar um professor
@app.route('/professores/<int:id_professor>', methods=['DELETE'])
def deletar_professor(id_professor):
    professor = Professor.query.get_or_404(id_professor)
    db.session.delete(professor)
    db.session.commit()
    return jsonify({'message': 'Professor deletado com sucesso!'})
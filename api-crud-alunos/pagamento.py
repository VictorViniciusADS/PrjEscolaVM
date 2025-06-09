# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

    #codigo para pagamentos
from flask import Flask, request, jsonify
from models import db, Pagamento

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Banco de dados SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Modelo Pagamento
class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    referencia = db.Column(db.String(100), nullable=True)

# Rota para listar pagamentos
@app.route('/pagamentos', methods=['GET'])
def listar_pagamentos():
    pagamentos = Pagamento.query.all()
    return jsonify([{
        'id_pagamento': pagamento.id_pagamento,
        'id_aluno': pagamento.id_aluno,
        'data_pagamento': str(pagamento.data_pagamento),
        'valor_pago': pagamento.valor_pago,
        'forma_pagamento': pagamento.forma_pagamento,
        'referencia': pagamento.referencia
    } for pagamento in pagamentos])

# Rota para criar um novo pagamento
@app.route('/pagamentos', methods=['POST'])
def criar_pagamento():
    dados = request.json
    novo_pagamento = Pagamento(
        id_aluno=dados['id_aluno'],
        data_pagamento=dados['data_pagamento'],
        valor_pago=dados['valor_pago'],
        forma_pagamento=dados['forma_pagamento'],
        referencia=dados.get('referencia')
    )
    db.session.add(novo_pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento criado com sucesso!'}), 201

# Rota para atualizar um pagamento
@app.route('/pagamentos/<int:id_pagamento>', methods=['PUT'])
def atualizar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    dados = request.json
    pagamento.id_aluno = dados['id_aluno']
    pagamento.data_pagamento = dados['data_pagamento']
    pagamento.valor_pago = dados['valor_pago']
    pagamento.forma_pagamento = dados['forma_pagamento']
    pagamento.referencia = dados.get('referencia')
    db.session.commit()
    return jsonify({'message': 'Pagamento atualizado com sucesso!'})

# Rota para deletar um pagamento
@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def deletar_pagamento(id_pagamento):
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento deletado com sucesso!'})
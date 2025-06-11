from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger 

# Inicialização e Configuração 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Configuração do Swagger 
app.config['SWAGGER'] = {
    'title': 'API de Pagamentos',
    'uiversion': 3,
    'version': '1.0',
    'description': 'API para registrar e gerenciar pagamentos de alunos.'
}
# Inicializa as extensões
db = SQLAlchemy(app)
swagger = Swagger(app)

# Definição do Modelo (Model)
class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aluno_id = db.Column(db.Integer, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    referencia = db.Column(db.String(100), nullable=True)

#  Definição das Rotas (Endpoints) 

# Rota para listar pagamentos
@app.route('/pagamentos', methods=['GET'])
def listar_pagamentos():
    """
    Lista todos os pagamentos registrados.
    ---
    tags:
      - Pagamentos
    summary: Retorna uma lista com todos os registros de pagamento.
    responses:
      200:
        description: Lista de pagamentos retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_pagamento:
                type: integer
              id_aluno:
                type: integer
              data_pagamento:
                type: string
                format: date
              valor_pago:
                type: number
                format: float
              forma_pagamento:
                type: string
              referencia:
                type: string
    """
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
    """
    Registra um novo pagamento.
    ---
    tags:
      - Pagamentos
    summary: Adiciona um novo registro de pagamento na base de dados.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - id_aluno
            - data_pagamento
            - valor_pago
            - forma_pagamento
          properties:
            id_aluno:
              type: integer
              description: ID do aluno que realizou o pagamento.
            data_pagamento:
              type: string
              format: date
              description: Data em que o pagamento foi efetuado (YYYY-MM-DD).
            valor_pago:
              type: number
              format: float
              description: O valor que foi pago.
            forma_pagamento:
              type: string
              description: "Método de pagamento (ex: 'Cartão de Crédito', 'Boleto', 'PIX')."
            referencia:
              type: string
              description: "Referência do pagamento (ex: 'Mensalidade Maio/2025'). Opcional."
    responses:
      201:
        description: Pagamento criado com sucesso.
    """
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
    """
    Atualiza um pagamento existente.
    ---
    tags:
      - Pagamentos
    summary: Atualiza os dados de um pagamento pelo seu ID.
    parameters:
      - name: id_pagamento
        in: path
        type: integer
        required: true
        description: ID do pagamento a ser atualizado.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            id_aluno:
              type: integer
            data_pagamento:
              type: string
              format: date
            valor_pago:
              type: number
              format: float
            forma_pagamento:
              type: string
            referencia:
              type: string
    responses:
      200:
        description: Pagamento atualizado com sucesso.
      404:
        description: Pagamento não encontrado.
    """
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    dados = request.json
    pagamento.id_aluno = dados.get('id_aluno', pagamento.id_aluno)
    pagamento.data_pagamento = dados.get('data_pagamento', pagamento.data_pagamento)
    pagamento.valor_pago = dados.get('valor_pago', pagamento.valor_pago)
    pagamento.forma_pagamento = dados.get('forma_pagamento', pagamento.forma_pagamento)
    pagamento.referencia = dados.get('referencia', pagamento.referencia)
    db.session.commit()
    return jsonify({'message': 'Pagamento atualizado com sucesso!'})

# Rota para deletar um pagamento
@app.route('/pagamentos/<int:id_pagamento>', methods=['DELETE'])
def deletar_pagamento(id_pagamento):
    """
    Exclui um registro de pagamento.
    tags:
      - Pagamentos
    summary: Remove um pagamento da base de dados pelo seu ID.
    parameters:
      - name: id_pagamento
        in: path
        type: integer
        required: true
        description: ID do pagamento a ser deletado.
    responses:
      200:
        description: Pagamento deletado com sucesso.
      404:
        description: Pagamento não encontrado.
    """
    pagamento = Pagamento.query.get_or_404(id_pagamento)
    db.session.delete(pagamento)
    db.session.commit()
    return jsonify({'message': 'Pagamento deletado com sucesso!'})


# Execução da Aplicação
# Inicializa o banco de dados (cria as tabelas se não existirem)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
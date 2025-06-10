from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger 

#  Inicialização e Configuração 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Swagger 
app.config['SWAGGER'] = {
    'title': 'API de Atividades',
    'uiversion': 3,
    'version': '1.0',
    'description': 'Uma API simples para gerenciar atividades (criar, ler, atualizar e deletar).'
}
# Inicializa as extensões
db = SQLAlchemy(app)
swagger = Swagger(app)

#  Definição do Modelo
class Atividade(db.Model):
    __tablename__ = 'atividade'
    id_atividade = db.Column(db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column(db.String(255), nullable=False)
    data_realizacao = db.Column(db.Date, nullable=False)

# Definição das Rotas (Endpoints)

# Rota para listar todas as atividades
@app.route('/atividades', methods=['GET'])
def listar_atividades():
    """
    Lista todas as atividades cadastradas.
    ---
    tags:
      - Atividades
    summary: Retorna uma lista com todas as atividades.
    responses:
      200:
        description: Lista de atividades retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_atividade:
                type: integer
              descricao:
                type: string
              data_realizacao:
                type: string
                format: date
    """
    atividades = Atividade.query.all()
    return jsonify([{
        'id_atividade': atividade.id_atividade,
        'descricao': atividade.descricao,
        'data_realizacao': str(atividade.data_realizacao)
    } for atividade in atividades])

# Rota para criar uma nova atividade
@app.route('/atividades', methods=['POST'])
def criar_atividade():
    """
    Cria uma nova atividade.
    ---
    tags:
      - Atividades
    summary: Adiciona uma nova atividade na base de dados.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - descricao
            - data_realizacao
          properties:
            descricao:
              type: string
              description: A descrição da atividade.
            data_realizacao:
              type: string
              format: date
              description: A data de realização (formato YYYY-MM-DD).
    responses:
      201:
        description: Atividade criada com sucesso.
    """
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
    """
    Atualiza uma atividade existente.
    ---
    tags:
      - Atividades
    summary: Atualiza a descrição e a data de uma atividade pelo seu ID.
    parameters:
      - name: id_atividade
        in: path
        type: integer
        required: true
        description: ID da atividade a ser atualizada.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            descricao:
              type: string
            data_realizacao:
              type: string
              format: date
    responses:
      200:
        description: Atividade atualizada com sucesso.
      404:
        description: Atividade não encontrada.
    """
    atividade = Atividade.query.get_or_404(id_atividade)
    dados = request.json
    atividade.descricao = dados.get('descricao', atividade.descricao)
    atividade.data_realizacao = dados.get('data_realizacao', atividade.data_realizacao)
    db.session.commit()
    return jsonify({'message': 'Atividade atualizada com sucesso!'})

# Rota para deletar uma atividade
@app.route('/atividades/<int:id_atividade>', methods=['DELETE'])
def deletar_atividade(id_atividade):
    """
    Deleta uma atividade existente.
    ---
    tags:
      - Atividades
    summary: Remove uma atividade da base de dados pelo seu ID.
    parameters:
      - name: id_atividade
        in: path
        type: integer
        required: true
        description: ID da atividade a ser deletada.
    responses:
      200:
        description: Atividade deletada com sucesso.
      404:
        description: Atividade não encontrada.
    """
    atividade = Atividade.query.get_or_404(id_atividade)
    db.session.delete(atividade)
    db.session.commit()
    return jsonify({'message': 'Atividade deletada com sucesso!'})

#  Execução da Aplicação
# Inicializa o banco de dados (cria as tabelas se não existirem)
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
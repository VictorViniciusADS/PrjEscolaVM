from flask import Flask, request, jsonify
from flasgger import Swagger  
from models import db, Aluno 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Swagger ---
app.config['SWAGGER'] = {
    'title': 'API de Alunos',
    'uiversion': 3,
    'version': '1.0',
    'description': 'API para gerenciar o cadastro de alunos.'
}
swagger = Swagger(app) # Inicializa o Swagger com a aplicação


db.init_app(app)

# Foi removida a criação automática do banco de dados para evitar problemas de compatibilidade com o SQLite.


# Listar Alunos Cadastrados (READ)
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    """
    Lista todos os alunos cadastrados.
    ---
    tags:
      - Alunos
    summary: Retorna uma lista com todos os alunos.
    responses:
      200:
        description: Lista de alunos retornada com sucesso.
        schema:
          type: array
          items:
            type: object
            properties:
              id_aluno:
                type: integer
              nome_completo:
                type: string
              data_nascimento:
                type: string
                format: date
              id_turma:
                type: integer
              nome_responsavel:
                type: string
              telefone_responsavel:
                type: string
              email_responsavel:
                type: string
              informacoes_adicionais:
                type: string
    """
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
    """
    Cadastra um novo aluno no sistema.
    ---
    tags:
      - Alunos
    summary: Adiciona um novo aluno à base de dados.
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
              description: Nome completo do aluno.
            data_nascimento:
              type: string
              format: date
              description: Data de nascimento (YYYY-MM-DD).
            id_turma:
              type: integer
              description: ID da turma do aluno.
            nome_responsavel:
              type: string
              description: Nome do responsável pelo aluno.
            telefone_responsavel:
              type: string
              description: Telefone do responsável.
            email_responsavel:
              type: string
              format: email
              description: E-mail do responsável.
            informacoes_adicionais:
              type: string
              description: Informações adicionais (opcional).
    responses:
      201:
        description: Aluno cadastrado com sucesso.
      400:
        description: Dados inválidos fornecidos.
    """
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
@app.route('/alunos/<int:aluno_id>', methods=['PUT'])
def alterar_aluno(aluno_id):
    """
    Altera os dados de um aluno existente.
    ---
    tags:
      - Alunos
    summary: Atualiza os dados de um aluno a partir do seu ID.
    parameters:
      - in: path
        name: aluno_id
        type: integer
        required: true
        description: ID único do aluno a ser alterado.
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            nome_completo:
              type: string
            data_nascimento:
              type: string
              format: date
            id_turma:
              type: integer
            nome_responsavel:
              type: string
            telefone_responsavel:
              type: string
            email_responsavel:
              type: string
            informacoes_adicionais:
              type: string
    responses:
      200:
        description: Dados do aluno atualizados com sucesso.
      404:
        description: Aluno não encontrado.
    """
    aluno = Aluno.query.get(aluno_id)
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
@app.route('/alunos/<int:aluno_id>', methods=['DELETE'])
def excluir_aluno(aluno_id):
    """
    Exclui um aluno do sistema.
    ---
    tags:
      - Alunos
    summary: Remove um aluno da base de dados a partir do seu ID.
    parameters:
      - in: path
        name: aluno_id
        type: integer
        required: true
        description: ID único do aluno a ser excluído.
    responses:
      200:
        description: Aluno excluído com sucesso.
      404:
        description: Aluno não encontrado.
    """
    aluno = Aluno.query.get(aluno_id)
    if not aluno:
        return jsonify({"message": "Aluno não encontrado!"}), 404

    db.session.delete(aluno)
    db.session.commit()
    return jsonify({"message": "Aluno excluído com sucesso!"})
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from models import db, Turma 

app = Flask(__name__)

# Configurações da Aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Swagger
swagger = Swagger(app)

db.init_app(app)


# Rota para listar todas as turmas
@app.route('/turmas', methods=['GET'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Retorna uma lista de todas as turmas cadastradas.',
    'responses': {
        '200': {
            'description': 'Uma lista de turmas.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_turma': {'type': 'integer'},
                        'nome_turma': {'type': 'string'},
                        'id_professor': {'type': 'integer'},
                        'horario': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def listar_turmas():
    """Retorna todas as turmas."""
    turmas = Turma.query.all()
    return jsonify([{
        'id_turma': turma.id_turma,
        'nome_turma': turma.nome_turma,
        'id_professor': turma.id_professor,
        'horario': turma.horario
    } for turma in turmas])

# Rota para criar uma nova turma
@app.route('/turmas', methods=['POST'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Cria uma nova turma.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_turma': {'type': 'string', 'example': 'Turma de Algoritmos I'},
                    'id_professor': {'type': 'integer', 'example': 1},
                    'horario': {'type': 'string', 'example': 'Seg/Qua 19:00-21:00'}
                },
                'required': ['nome_turma', 'id_professor', 'horario']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Turma criada com sucesso.'
        }
    }
})
def criar_turma():
    """Cria uma nova turma."""
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
@swag_from({
    'tags': ['Turmas'],
    'description': 'Atualiza uma turma existente.',
    'parameters': [
        {
            'name': 'id_turma',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da turma a ser atualizada.'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'nome_turma': {'type': 'string'},
                    'id_professor': {'type': 'integer'},
                    'horario': {'type': 'string'}
                },
                'required': ['nome_turma', 'id_professor', 'horario']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Turma atualizada com sucesso.'
        },
        '404': {
            'description': 'Turma não encontrada.'
        }
    }
})
def atualizar_turma(id_turma):
    """Atualiza uma turma existente."""
    turma = Turma.query.get_or_404(id_turma)
    dados = request.json
    turma.nome_turma = dados.get('nome_turma', turma.nome_turma)
    turma.id_professor = dados.get('id_professor', turma.id_professor)
    turma.horario = dados.get('horario', turma.horario)
    db.session.commit()
    return jsonify({'message': 'Turma atualizada com sucesso!'})

# Rota para deletar uma turma
@app.route('/turmas/<int:id_turma>', methods=['DELETE'])
@swag_from({
    'tags': ['Turmas'],
    'description': 'Deleta uma turma.',
    'parameters': [
        {
            'name': 'id_turma',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da turma a ser deletada.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Turma deletada com sucesso.'
        },
        '404': {
            'description': 'Turma não encontrada.'
        }
    }
})
def deletar_turma(id_turma):
    """Deleta uma turma."""
    turma = Turma.query.get_or_404(id_turma)
    db.session.delete(turma)
    db.session.commit()
    return jsonify({'message': 'Turma deletada com sucesso!'})

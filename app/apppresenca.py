from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from models import db, Presenca

app = Flask(__name__)

# Configurações da Aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Swagger
swagger = Swagger(app)

db.init_app(app)


# Rota para listar todas as presenças
@app.route('/presencas', methods=['GET'])
@swag_from({
    'tags': ['Presenças'],
    'description': 'Retorna uma lista de todas as presenças registradas.',
    'responses': {
        '200': {
            'description': 'Uma lista de presenças.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_presenca': {'type': 'integer'},
                        'id_aluno': {'type': 'integer'},
                        'data_presenca': {'type': 'string', 'format': 'date'},
                        'presente': {'type': 'boolean'}
                    }
                }
            }
        }
    }
})
def listar_presencas():
    """Retorna todas as presenças."""
    presencas = Presenca.query.all()
    return jsonify([{
        'id_presenca': presenca.id_presenca,
        'id_aluno': presenca.id_aluno,
        'data_presenca': str(presenca.data_presenca),
        'presente': presenca.presente
    } for presenca in presencas])

# Rota para criar uma nova presença
@app.route('/presencas', methods=['POST'])
@swag_from({
    'tags': ['Presenças'],
    'description': 'Cria um novo registro de presença.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_aluno': {'type': 'integer', 'example': 101},
                    'data_presenca': {'type': 'string', 'format': 'date', 'example': '2025-06-10'},
                    'presente': {'type': 'boolean', 'example': True}
                },
                'required': ['id_aluno', 'data_presenca', 'presente']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Presença criada com sucesso.'
        }
    }
})
def criar_presenca():
    """Cria uma nova presença."""
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
@swag_from({
    'tags': ['Presenças'],
    'description': 'Atualiza um registro de presença existente.',
    'parameters': [
        {
            'name': 'id_presenca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da presença a ser atualizada.'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id_aluno': {'type': 'integer'},
                    'data_presenca': {'type': 'string', 'format': 'date'},
                    'presente': {'type': 'boolean'}
                }
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Presença atualizada com sucesso.'
        },
        '404': {
            'description': 'Presença não encontrada.'
        }
    }
})
def atualizar_presenca(id_presenca):
    """Atualiza uma presença existente."""
    presenca = Presenca.query.get_or_404(id_presenca)
    dados = request.json
    presenca.id_aluno = dados.get('id_aluno', presenca.id_aluno)
    presenca.data_presenca = dados.get('data_presenca', presenca.data_presenca)
    presenca.presente = dados.get('presente', presenca.presente)
    db.session.commit()
    return jsonify({'message': 'Presença atualizada com sucesso!'})

# Rota para deletar uma presença
@app.route('/presencas/<int:id_presenca>', methods=['DELETE'])
@swag_from({
    'tags': ['Presenças'],
    'description': 'Deleta um registro de presença.',
    'parameters': [
        {
            'name': 'id_presenca',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID da presença a ser deletada.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Presença deletada com sucesso.'
        },
        '404': {
            'description': 'Presença não encontrada.'
        }
    }
})
def deletar_presenca(id_presenca):
    """Deleta uma presença existente."""
    presenca = Presenca.query.get_or_404(id_presenca)
    db.session.delete(presenca)
    db.session.commit()
    return jsonify({'message': 'Presença deletada com sucesso!'})

# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
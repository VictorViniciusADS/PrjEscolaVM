from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from
from models import db, Usuario 

app = Flask(__name__)

# Configurações da Aplicação
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin@db:5432/escola'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuração do Swagger
swagger = Swagger(app)

db.init_app(app)

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Retorna uma lista de todos os usuários. A senha não é retornada.',
    'responses': {
        '200': {
            'description': 'Uma lista de usuários.',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id_usuario': {'type': 'integer'},
                        'login': {'type': 'string'},
                        'nivel_acesso': {'type': 'string'},
                        'id_professor': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def listar_usuarios():
    """Retorna todos os usuários (sem a senha)."""
    usuarios = Usuario.query.all()
    return jsonify([{
        'id_usuario': usuario.id_usuario,
        'login': usuario.login,
        'nivel_acesso': usuario.nivel_acesso,
        'id_professor': usuario.id_professor
    } for usuario in usuarios])

# Rota para criar um novo usuário
@app.route('/usuarios', methods=['POST'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Cria um novo usuário. A senha deve ser fornecida.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'string', 'example': 'joao.silva'},
                    'senha': {'type': 'string', 'format': 'password', 'example': 'senhaSuperSecreta123'},
                    'nivel_acesso': {'type': 'string', 'example': 'professor'},
                    'id_professor': {'type': 'integer', 'example': 1}
                },
                'required': ['login', 'senha', 'nivel_acesso']
            }
        }
    ],
    'responses': {
        '201': {
            'description': 'Usuário criado com sucesso.'
        }
    }
})
def criar_usuario():
    """Cria um novo usuário."""
    dados = request.json
    
    novo_usuario = Usuario(
        login=dados['login'],
        senha=dados['senha'], 
        nivel_acesso=dados['nivel_acesso'],
        id_professor=dados.get('id_professor')
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

# Rota para atualizar um usuário existente
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Atualiza um usuário existente.',
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser atualizado.'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'login': {'type': 'string'},
                    'senha': {'type': 'string', 'format': 'password'},
                    'nivel_acesso': {'type': 'string'},
                    'id_professor': {'type': 'integer'}
                },
                'required': ['login', 'senha', 'nivel_acesso']
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuário atualizado com sucesso.'
        },
        '404': {
            'description': 'Usuário não encontrado.'
        }
    }
})
def atualizar_usuario(id_usuario):
    """Atualiza um usuário existente."""
    usuario = Usuario.query.get_or_404(id_usuario)
    dados = request.json
    usuario.login = dados.get('login', usuario.login)
    usuario.senha = dados.get('senha', usuario.senha) # Lembre-se de gerar o hash
    usuario.nivel_acesso = dados.get('nivel_acesso', usuario.nivel_acesso)
    usuario.id_professor = dados.get('id_professor', usuario.id_professor)
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso!'})

# Rota para deletar um usuário
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@swag_from({
    'tags': ['Usuários'],
    'description': 'Deleta um usuário.',
    'parameters': [
        {
            'name': 'id_usuario',
            'in': 'path',
            'type': 'integer',
            'required': True,
            'description': 'ID do usuário a ser deletado.'
        }
    ],
    'responses': {
        '200': {
            'description': 'Usuário deletado com sucesso.'
        },
        '404': {
            'description': 'Usuário não encontrado.'
        }
    }
})
def deletar_usuario(id_usuario):
    """Deleta um usuário."""
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso!'})

# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
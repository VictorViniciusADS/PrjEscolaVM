# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify
from models import db, Usuario    

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///meu_banco.db'  # Banco SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        'id_usuario': usuario.id_usuario,
        'login': usuario.login,
        'nivel_acesso': usuario.nivel_acesso,
        'id_professor': usuario.id_professor
    } for usuario in usuarios])

# Rota para criar um novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    novo_usuario = Usuario(
        login=dados['login'],
        senha=dados['senha'],  # Idealmente, use uma função de hash para senhas
        nivel_acesso=dados['nivel_acesso'],
        id_professor=dados.get('id_professor')  # Opcional
    )
    db.session.add(novo_usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'}), 201

# Rota para atualizar um usuário existente
@app.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def atualizar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    dados = request.json
    usuario.login = dados['login']
    usuario.senha = dados['senha']  # Atualize com a senha hash aqui
    usuario.nivel_acesso = dados['nivel_acesso']
    usuario.id_professor = dados.get('id_professor')  # Opcional
    db.session.commit()
    return jsonify({'message': 'Usuário atualizado com sucesso!'})

# Rota para deletar um usuário
@app.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
def deletar_usuario(id_usuario):
    usuario = Usuario.query.get_or_404(id_usuario)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({'message': 'Usuário deletado com sucesso!'})

# Inicializar o banco de dados
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
    
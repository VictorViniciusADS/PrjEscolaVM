from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Modelo Aluno
class Aluno(db.Model):
    __tablename__ = 'aluno'
    id_aluno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    id_turma = db.Column(db.Integer, nullable=False)
    nome_responsavel = db.Column(db.String(255), nullable=False)
    telefone_responsavel = db.Column(db.String(20), nullable=False)
    email_responsavel = db.Column(db.String(100), nullable=False)
    informacoes_adicionais = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Aluno {self.nome_completo}>'

# Modelo Turma
class Turma(db.Model):
    __tablename__ = 'turma'
    id_turma = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_turma = db.Column(db.String(50), nullable=False)  # Corrigido para VARCHAR(50)
    id_professor = db.Column(db.Integer, nullable=False)
    horario = db.Column(db.String(100), nullable=False)    # Corrigido para VARCHAR(100)

# Modelo Professor
class Professor(db.Model):
    __tablename__ = 'professor'
    id_professor = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefone = db.Column(db.String(20), nullable=False)

# Modelo Pagamento
class Pagamento(db.Model):
    __tablename__ = 'pagamento'
    id_pagamento = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, nullable=False)
    data_pagamento = db.Column(db.Date, nullable=False)
    valor_pago = db.Column(db.Float, nullable=False)
    forma_pagamento = db.Column(db.String(50), nullable=False)
    referencia = db.Column(db.String(100), nullable=True)

# Modelo Presenca
class Presenca(db.Model):
    __tablename__ = 'presenca'
    id_presenca = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_aluno = db.Column(db.Integer, nullable=False)
    data_presenca = db.Column(db.Date, nullable=False)
    presente = db.Column(db.Boolean, nullable=False)

# Modelo AtividadeAluno
class AtividadeAluno(db.Model):
    __tablename__ = 'atividade_aluno'
    id_atividade = db.Column(db.Integer, primary_key=True)
    id_aluno = db.Column(db.Integer, primary_key=True)

# Modelo Usuario
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    login = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(255), nullable=False)
    nivel_acesso = db.Column(db.String(20), nullable=False)
    id_professor = db.Column(db.Integer, db.ForeignKey('professor.id_professor'), nullable=True)

    professor = db.relationship('Professor', backref='usuarios')
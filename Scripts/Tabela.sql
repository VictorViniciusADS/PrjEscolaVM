Table professor {
    id_professor SERIAL [pk]
    nome_completo VARCHAR(255)
    email VARCHAR(100)
    telefone VARCHAR(20)
}

Table turma {
    id_turma SERIAL [pk]
    nome_turma VARCHAR(100)
    id_professor INTEGER [ref: > professor.id_professor]
    horario VARCHAR(50)
}

Table aluno {
    id_aluno SERIAL [pk]
    nome_completo VARCHAR(255)
    data_nascimento DATE
    id_turma INTEGER [ref: > turma.id_turma]
    nome_responsavel VARCHAR(255)
    telefone_responsavel VARCHAR(20)
    email_responsavel VARCHAR(100)
    informacoes_adicionais TEXT
}

Table pagamento {
    id_pagamento SERIAL [pk]
    id_aluno INTEGER [ref: > aluno.id_aluno]
    data_pagamento DATE
    valor_pago NUMERIC(10,2)
    forma_pagamento VARCHAR(50)
    referencia VARCHAR(100)
}

Table presenca {
    id_presenca SERIAL [pk]
    id_aluno INTEGER [ref: > aluno.id_aluno]
    data_presenca DATE
    presente BOOLEAN
}

Table atividade {
    id_atividade SERIAL [pk]
    descricao VARCHAR(255)
    data_atividade DATE
}

Table atividade_aluno {
    id_atividade INTEGER [ref: > atividade.id_atividade]
    id_aluno INTEGER [ref: > aluno.id_aluno]
    [pk]
}

Table usuario {
    id_usuario SERIAL [pk]
    login VARCHAR(50) [unique]
    senha VARCHAR(255)
    nivel_acesso VARCHAR(50)
    id_professor INTEGER [ref: > professor.id_professor]
}
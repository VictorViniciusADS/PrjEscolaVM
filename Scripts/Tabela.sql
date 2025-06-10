-- Tabela que armazena informações dos professores
Table professor {
    id_professor SERIAL [pk] -- Identificador único do professor (chave primária)
    nome_completo VARCHAR(255) -- Nome completo do professor
    email VARCHAR(100) -- Email do professor
    telefone VARCHAR(20) -- Telefone do professor
}

-- Tabela que armazena informações das turmas
Table turma {
    id_turma SERIAL [pk] -- Identificador único da turma (chave primária)
    nome_turma VARCHAR(100) -- Nome da turma
    id_professor INTEGER [ref: > professor.id_professor] -- Professor responsável pela turma (chave estrangeira)
    horario VARCHAR(50) -- Horário da turma
}

-- Tabela que armazena informações dos alunos
Table aluno {
    id_aluno SERIAL [pk] -- Identificador único do aluno (chave primária)
    nome_completo VARCHAR(255) -- Nome completo do aluno
    data_nascimento DATE -- Data de nascimento do aluno
    id_turma INTEGER [ref: > turma.id_turma] -- Turma a qual o aluno pertence (chave estrangeira)
    nome_responsavel VARCHAR(255) -- Nome do responsável pelo aluno
    telefone_responsavel VARCHAR(20) -- Telefone do responsável
    email_responsavel VARCHAR(100) -- Email do responsável
    informacoes_adicionais TEXT -- Informações adicionais sobre o aluno
}

-- Tabela que armazena informações de pagamentos
Table pagamento {
    id_pagamento SERIAL [pk] -- Identificador único do pagamento (chave primária)
    id_aluno INTEGER [ref: > aluno.id_aluno] -- Aluno relacionado ao pagamento (chave estrangeira)
    data_pagamento DATE -- Data do pagamento
    valor_pago NUMERIC(10,2) -- Valor pago pelo aluno
    forma_pagamento VARCHAR(50) -- Forma de pagamento utilizada
    referencia VARCHAR(100) -- Referência do pagamento
}

-- Tabela que armazena registros de presença dos alunos
Table presenca {
    id_presenca SERIAL [pk] -- Identificador único da presença (chave primária)
    id_aluno INTEGER [ref: > aluno.id_aluno] -- Aluno relacionado à presença (chave estrangeira)
    data_presenca DATE -- Data em que a presença foi registrada
    presente BOOLEAN -- Indica se o aluno estava presente (true ou false)
}

-- Tabela que armazena as atividades realizadas
Table atividade {
    id_atividade SERIAL [pk] -- Identificador único da atividade (chave primária)
    descricao VARCHAR(255) -- Descrição da atividade
    data_atividade DATE -- Data em que a atividade ocorreu
}

--Tabela intermediária que relaciona atividades com alunos
Table atividade_aluno {
    id_atividade INTEGER [ref: > atividade.id_atividade] -- Identificador da atividade (chave estrangeira)
    id_aluno INTEGER [ref: > aluno.id_aluno] -- Identificador do aluno (chave estrangeira)
    [pk] -- Chave primária composta (id_atividade, id_aluno)
}

-- Tabela que armazena informações dos usuários do sistema
Table usuario {
    id_usuario SERIAL [pk] -- Identificador único do usuário (chave primária)
    login VARCHAR(50) [unique] -- Login do usuário (único)
    senha VARCHAR(255) -- Senha do usuário
    nivel_acesso VARCHAR(50) -- Nível de acesso do usuário ao sistema
    id_professor INTEGER [ref: > professor.id_professor] -- Relacionamento opcional com professor
}

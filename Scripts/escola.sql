-- DDL Sistema de Gestão Escolar

-- Criação da tabela de Alunos
CREATE TABLE alunos (
    matricula INT PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    data_nascimento DATE,
    endereco VARCHAR(255),
    contato_pais_responsaveis VARCHAR(255)
);

-- Criação da tabela de Professores
CREATE TABLE professores (
    registro INT PRIMARY KEY,
    nome_completo VARCHAR(255) NOT NULL,
    especialidade VARCHAR(100),
    contato VARCHAR(100)
);

-- Criação da tabela de Disciplinas
CREATE TABLE disciplinas (
    codigo VARCHAR(10) PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    carga_horaria INT NOT NULL
);

-- Criação da tabela de Turmas
CREATE TABLE turmas (
    id_turma INT PRIMARY KEY AUTO_INCREMENT,
    identificacao VARCHAR(50) NOT NULL,
    ano_letivo VARCHAR(10) NOT NULL
);

-- Criação da tabela de Matrículas
CREATE TABLE matricula (
    id_matricula INT PRIMARY KEY AUTO_INCREMENT,
    matricula_aluno INT NOT NULL,
    id_turma_fk INT NOT NULL,
    data_matricula DATE NOT NULL,
    FOREIGN KEY (matricula_aluno) REFERENCES alunos(matricula),
    FOREIGN KEY (id_turma_fk) REFERENCES turmas(id_turma),
    UNIQUE (matricula_aluno, id_turma_fk)
);

-- Criação da tabela de Notas e Frequência
CREATE TABLE notas_frequencia (
    id_registro INT PRIMARY KEY AUTO_INCREMENT,
    matricula_aluno_fk INT NOT NULL,
    codigo_disciplina_fk VARCHAR(10) NOT NULL,
    id_turma_fk INT NOT NULL,
    nota DECIMAL(4, 2),
    frequencia DECIMAL(5, 2),
    FOREIGN KEY (matricula_aluno_fk) REFERENCES alunos(matricula),
    FOREIGN KEY (codigo_disciplina_fk) REFERENCES disciplinas(codigo),
    FOREIGN KEY (id_turma_fk) REFERENCES turmas(id_turma),
    UNIQUE (matricula_aluno_fk, codigo_disciplina_fk, id_turma_fk)
);

-- Criação da tabela de Turmas e Disciplinas
CREATE TABLE turmas_disciplinas (
    id_turma_fk INT NOT NULL,
    codigo_disciplina_fk VARCHAR(10) NOT NULL,
    registro_professor_fk INT,
    PRIMARY KEY (id_turma_fk, codigo_disciplina_fk),
    FOREIGN KEY (id_turma_fk) REFERENCES turmas(id_turma),
    FOREIGN KEY (codigo_disciplina_fk) REFERENCES disciplinas(codigo),
    FOREIGN KEY (registro_professor_fk) REFERENCES professores(registro)
);

-- Com a atividade de hoje fui elucidado da forma como o funciona o ecosistema do banco de dados entre as tabelas e as colunas.Sendo a tabela o local onde guardamos as informações especificas da lista como exemplo 'alunos' e 'professores' e dentro dessas tabelas nos iformamos itens mais especificos para ajudar a catalogar como por exemplo 
-- dentro de alunos podemos colocar 'nome' e 'data de nascimento' e dentro das colunas nos especificamos melhor o tipo de informação que ela possui sendo ela um texto ou até mesmo um número. E apos isso na ativdidae nos fizemos a ligação entre essas informações para que o sistema tenha meios mais abrangentes de achar os resultados.QUanto mais informações forem precisadas no arquivo mais fácil ele sera de ser reproduzido ou atualizado.
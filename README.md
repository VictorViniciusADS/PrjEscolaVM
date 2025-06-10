# PrjEscolaVM
Projeto Integração e Implementação de Software para o fim do semestre 
Alunos
Victor Vinicius Ramos Pinheiro de Almeida - RA 6323096
Murilo Marchesini de Camargo - RA 6320051

# Descrição
Este projeto é um sistema de gestão escolar desenvolvido em Python com Flask, utilizando PostgreSQL como banco de dados e Docker para orquestração dos serviços. O backend expõe APIs RESTful para gerenciamento de alunos, professores, turmas, presenças, pagamentos, atividades e usuários.

# Pré-Requisitos
Git
Docker
Docker Compose

# Passo a Passo para Configuração e Execução
1. Clonagem do Repositório - Abra o terminal e execute:
   git clone https://github.com/VictorViniciusADS/PrjEscolaVM.git

2. Configuração de Ambiente - Certifique-se de que as portas 5000 (API) e 5432 (PostgreSQL) estejam livres. (Não é necessário configurar variáveis de ambiente manualmente, pois já estão definidas no docker-compose.yml)

3. Build dos Containers - Execute o comando a seguir para construir as imagens Docker dos serviços: docker-compose build

4. Inicialização dos Serviços - Suba os containers com:  docker-compose up
(Aguarde até que os serviços estejam totalmente inicializados. O banco de dados será criado automaticamente e os scripts de inicialização serão aplicados)

5. Acesso ao Backend - API Flask: em http://localhost:5000

6. Banco de Dados PostgreSQL: Host: localhost ---- Porta: 5432 ---- Usuário: admin ---- Senha: admin ---- Banco: escola (Você pode acessar o banco usando ferramentas como DBeaver, PgAdmin ou psql)

# ESTRUTURA DO PROJETO
````
PrjEscolaVM/
│
├── app/                
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   └── ... (outros módulos)
│
├── api-crud-alunos/    
│   └── ...
│
├── BD/                 
│   └── ...
│
├── Observabilidade/    
│   └── ...
│
├── docker-compose.yml  
├── Dockerfile          
└── README.md           
````

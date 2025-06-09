# Use a imagem oficial do PostgreSQL como base
FROM postgres:latest

# Defina variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_DB=mydatabase
ENV POSTGRES_USER=myuser
ENV POSTGRES_PASSWORD=mypassword

# Copie o script de inicialização para o diretório de inicialização do PostgreSQL
COPY init.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432
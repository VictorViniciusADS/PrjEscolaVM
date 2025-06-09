# Use a imagem oficial do PostgreSQL como base
FROM postgres:latest

# Defina variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_DB=init_escola
ENV POSTGRES_USER=faat
ENV POSTGRES_PASSWORD=faat

# Copie o script de inicialização para o diretório de inicialização do PostgreSQL
COPY init_escola.sql /docker-entrypoint-initdb.d/

# Exponha a porta padrão do PostgreSQL
EXPOSE 5432

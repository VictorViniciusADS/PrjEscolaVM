# Usa uma imagem base do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia os arquivos do projeto para o contêiner
COPY . /app

# Instala as dependências da aplicação
RUN pip install --no-cache-dir -r requirements.txt

# Define a variável de ambiente para o Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Exponha a porta 5000 para comunicação
EXPOSE 5000

# Comando para executar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
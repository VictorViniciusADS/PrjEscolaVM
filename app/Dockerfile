# Use uma imagem base do Python
FROM python:3.9-slim

# Defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo de dependências para o container
COPY requirements.txt requirements.txt

# Instale as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código do projeto para o container
COPY . .

# Exponha a porta que o Flask usará
EXPOSE 5000

# Comando para iniciar o aplicativo
CMD ["python", "app.py"]
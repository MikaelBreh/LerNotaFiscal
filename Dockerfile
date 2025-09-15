# ---- 1. Estágio de Construção (Build Stage) ----
# Usamos uma imagem base oficial do Python. A versão "slim" é mais leve. [cite: 173]
FROM python:3.12-slim as builder

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema, se necessário (ex: para pacotes como Pillow)
# RUN apt-get update && apt-get install -y gcc

# Copia o arquivo de dependências para o container
COPY requirements.txt .

# Instala as dependências do Python. Usar --no-cache-dir cria uma imagem menor.
RUN pip install --no-cache-dir -r requirements.txt


# ---- 2. Estágio Final (Final Stage) ----
# Começamos de novo com uma base limpa para a imagem final ser ainda menor
FROM python:3.12-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia as dependências instaladas do estágio de construção
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

# Copia todo o código da sua aplicação para o diretório de trabalho no container
COPY . .

# Expõe a porta 8000, que é a porta padrão do servidor de desenvolvimento do Django
EXPOSE 8000

# O comando que será executado quando o container iniciar.
# "0.0.0.0" permite que o servidor seja acessível de fora do container.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
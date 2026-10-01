# imagem base com Python
FROM python:3.12-slim

# diretório de trabalho dentro do container
WORKDIR /app

# dependências primeiro, para aproveitar o cache do Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# resto dos arquivos (app.py precisa do main.py junto)
COPY . .

# comando de inicialização
CMD ["python", "app.py"]
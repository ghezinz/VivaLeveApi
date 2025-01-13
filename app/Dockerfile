FROM python:3.10-slim

# Copie os arquivos necessários
WORKDIR /app
COPY ./app/requirements.txt /app/

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante da aplicação
COPY . /app/

# Exponha a porta e defina o comando para iniciar a aplicação
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


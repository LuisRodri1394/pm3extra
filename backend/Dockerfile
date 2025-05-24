FROM python:3.9-slim

# Instala dependências de sistema essenciais
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Configura um ambiente virtual mais seguro
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Primeiro copia apenas o requirements.txt para aproveitar cache Docker
COPY requirements.txt .

# Instala dependências com timeout aumentado e retry
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir --default-timeout=100 -r requirements.txt

# Copia o restante da aplicação
COPY . .

# Verifica se o arquivo principal existe
RUN test -f app.py || (echo "Arquivo app.py não encontrado!" && exit 1)

CMD ["gunicorn", "--bind", "0.0.0:5000", "--timeout", "120", "app:app"]
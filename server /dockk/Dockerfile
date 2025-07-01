FROM debian:bullseye

# Actualizar e instalar dependencias
RUN apt-get update && apt-get install -y \
    bash \
    gpm \
    python3 \
    python3-pip \
    python3-doc \
    python3-tk \
    python3-venv \
    python3.9-venv \
    python3.9-doc \
    binutils \
    binfmt-support \
    readline-doc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos locales al contenedor
COPY ./sample /app

# Instalar paquetes de Python
COPY ./sample/requirements.txt ./sample/dev_requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r dev_requirements.txt

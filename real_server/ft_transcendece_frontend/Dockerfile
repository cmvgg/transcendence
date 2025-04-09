FROM python:3.11-slim-buster

WORKDIR /appfront

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install djangorestframework

RUN python -m pip install Django

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    python3-dev \
    nano \
	curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
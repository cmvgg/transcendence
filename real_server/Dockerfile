FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install djangorestframework

RUN pip install django-crispy-forms


RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
	postgresql-client \
    python3-dev \
    nano \
	curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN python manage.py collectstatic --noinput

CMD ["python manage.py runserver 0.0.0.0:8000"]
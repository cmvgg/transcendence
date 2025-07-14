FROM python:3.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install djangorestframework django-crispy-forms django-prometheus

RUN pip install django-crispy-forms

RUN pip install python-json-logger

RUN pip install elasticsearch


RUN apt-get update && apt-get install -y --no-install-recommends \
	postgresql-client \
    libpq-dev \
    gcc \
    postgresql-client \
    postgresql-client \
    python3-dev \
    nano \
    curl \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
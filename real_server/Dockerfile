FROM python:3.11-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        python3-dev \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir \
        djangorestframework \
        django-prometheus \
        django-crispy-forms \
        python-json-logger \
        Pillow \
        passlib \
        django-resized

COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
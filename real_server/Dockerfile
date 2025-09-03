FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y --no-install-recommends postgresql-client 
RUN apt-get install -y --no-install-recommends libpq-dev 
RUN apt-get install -y --no-install-recommends python3-dev
RUN rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir djangorestframework
RUN pip install --no-cache-dir django-prometheus
RUN pip install --no-cache-dir django-crispy-forms
RUN pip install --no-cache-dir python-json-logger


RUN python -m pip install Pillow
RUN pip install passlib


COPY . .

CMD ["sh", "-c", "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"]
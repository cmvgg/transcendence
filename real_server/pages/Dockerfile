FROM python:3.11-slim

WORKDIR /appfront

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install djangorestframework

RUN python -m pip install Django

RUN mkdir /ft_transcendence_fronten/vol

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

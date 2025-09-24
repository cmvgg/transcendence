FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /appfront

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir djangorestframework Django

RUN mkdir -p /ft_transcendence_frontend/vol

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

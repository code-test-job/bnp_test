# syntax=docker/dockerfile:1
FROM python:3.9-slim-buster

# Configuration des variables d'environnement
ARG PYTHON_ENV
ARG API_USERNAME
ARG API_PASSWORD
ENV PYTHON_ENV=$PYTHON_ENV
ENV API_USERNAME=$API_USERNAME
ENV API_PASSWORD=$API_PASSWORD


# Installation des dépendances système nécessaires
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        nginx \
    && rm -rf /var/lib/apt/lists/*

# Création du répertoire de travail et copie des fichiers nécessaires
WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip \
    && pip3 install --no-cache-dir -r requirements.txt
COPY . .

# Exécution des tests avec pytest
RUN pytest

# Configuration de Nginx pour le filtrage web
COPY nginx.conf /etc/nginx/nginx.conf

# Configuration de l'API pour l'authentification
ENV API_USERNAME=$API_USERNAME
ENV API_PASSWORD=$API_PASSWORD

# Exposition du port de l'API
EXPOSE 5000

# Démarrage de Nginx en arrière-plan pour le filtrage web
CMD nginx && uvicorn app.main:app --host 0.0.0.0 --port 5000 --workers 4 --log-level=info

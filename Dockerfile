# Utilisation d'une image Python légère comme base
# FROM python:3.14.0a2-alpine3.20 AS base
FROM python:3.13-alpine3.21 AS base

# Configuration du répertoire de travail
WORKDIR /app

# Installation des outils de compilation nécessaires
RUN apk add --no-cache gcc g++ musl-dev jpeg-dev zlib-dev libjpeg make

# Installation des dépendances système nécessaires pour matplotlib
RUN apk add --no-cache freetype-dev libpng-dev

# Copie du fichier requirements.txt et installation des dépendances Python avec cache
COPY requirements.txt .
RUN pip install --no-cache-dir wheel
# montage d'un cache pour les dépendances du projet pour optimiser le temps du build - de 8-10 minutes à 3 secondes environ
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Copie du code source de l'application
COPY . .

# Installation de Node.js et npm
RUN apk add --no-cache nodejs npm

# Installation des dépendances npm
COPY package.json package-lock.json ./
RUN npm install

# Exposition du port 5000
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "run.py", "--host=0.0.0.0"]



# Étape 1 : Utiliser une image Python légère comme base
FROM python:3.14.0a2-alpine3.20 AS base

# Configurer le répertoire de travail
WORKDIR /app

# Installer les outils de compilation nécessaires
RUN apk add --no-cache gcc g++ musl-dev jpeg-dev zlib-dev libjpeg make

# Installer les dépendances système nécessaires pour matplotlib
RUN apk add --no-cache freetype-dev libpng-dev

# Copier le fichier requirements.txt et installer les dépendances Python avec cache
COPY requirements.txt .
RUN pip install --no-cache-dir wheel
# monte un cache pour les dépendances du projet pour optimiser le temps du build
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY . .

# Installer Node.js et npm
RUN apk add --no-cache nodejs npm

# Installer les dépendances npm
COPY package.json package-lock.json ./
RUN npm install

# Exposer le port 5000
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "run.py", "--host=0.0.0.0"]



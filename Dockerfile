# Utilisation d'une image Python légère comme base
# FROM python:3.14.0a2-alpine3.20 AS base
# FROM python:3.13-alpine3.21 AS base
FROM python:3.14.0a2-alpine3.21 AS base

# Configuration du répertoire de travail
WORKDIR /app

# Installation des outils de compilation nécessaires
RUN apk add --no-cache gcc g++ musl-dev jpeg-dev zlib-dev libjpeg make

# Installation des dépendances système nécessaires pour matplotlib
RUN apk add --no-cache freetype-dev libpng-dev

# Copie du fichier requirements.txt
COPY requirements.txt .

# # Mise à jour de pip et installation des dépendances spécifiées dans requirements.txt
# RUN pip install --no-cache-dir --upgrade pip \
#     && pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installation de wheel (bien que cela soit généralement inclus dans les dépendances)
RUN pip install --no-cache-dir wheel

# Gestion des dépendances Python en cache
RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt


# Installation de Jinja2 version 3.1
RUN pip install Jinja2==3.1

# Copie du code source de l'application
COPY . .

# Installation de Node.js et npm
RUN apk add --no-cache nodejs npm sqlite-dev

# Installation des dépendances npm
COPY package.json package-lock.json ./
RUN npm install

# # Installation de Trivy
# RUN apk add --no-cache curl \
#     && curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Exposition du port 5000
EXPOSE 5000


# Commande pour exécuter l'application
CMD ["python", "run.py", "--host=0.0.0.0"]

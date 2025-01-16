# Étape 1 : Utiliser une image Python légère comme base
FROM python:3.14.0a2-alpine3.20 AS base

# Configurer le répertoire de travail
WORKDIR /app

# Installer les outils de compilation nécessaires
RUN apk add --no-cache gcc g++ musl-dev jpeg-dev zlib-dev libjpeg make

# Installer les dépendances Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Installer les dépendances système nécessaires pour matplotlib
# RUN apk add --no-cache gcc musl-dev freetype-dev libpng-de
# RUN apk add --no-cache gcc g++ musl-dev
# installation de matplotlib
# RUN pip install matplotlib

# Afficher les dépendances installées
RUN pip freeze

# Copier le code source de l'application
# COPY flaskr /app/flaskr
# COPY run.py /app
# COPY requirements.txt /app
COPY . .


# Exposer le port 5000
EXPOSE 5000

# Commande pour exécuter l'application
CMD ["python", "run.py", "--host=0.0.0.0"]

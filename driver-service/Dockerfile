# Utiliser une image officielle de Python comme image de base
FROM python:3.9

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier requirements.txt dans le conteneur pour installer les dépendances
COPY driver-service/requirements.txt /app/requirements.txt

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le contenu du répertoire local dans le répertoire de travail du conteneur
COPY . /app/

# Définir la variable d'environnement pour la connexion à MongoDB
ENV MONGO_URI="mongodb://mongo:27017/driverdb"

# Exposer le port utilisé par l'application (si l'application utilise 3000, modifiez-le ici)
EXPOSE 3000

# Lancer l'application Python
CMD ["python", "app.py"]


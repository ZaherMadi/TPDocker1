FROM python:3.9

# Utilisateur non-root
RUN useradd -m -u 1000 appuser

WORKDIR /server

# Installer les dépendances en tant que root
COPY requirements.txt .
RUN pip install -r requirements.txt

# Changer la propriété du répertoire de travail
RUN chown -R appuser:appuser /server

# Passer à l'utilisateur non-root
USER appuser

EXPOSE 8000
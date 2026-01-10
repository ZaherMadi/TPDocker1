# Student Dashboard - Architecture Microservices

Projet de transformation d'un POC en stack de production résiliente et sécurisée.

## Architecture

```
┌──────────────┐
│   Frontend   │ :8080 (Nginx)
│  (Browser)   │
└──────┬───────┘
       │
┌──────▼───────┐
│     API      │ :8000 (FastAPI)
│   (Python)   │
└──┬────────┬──┘
   │        │
   │        │ backend_net
   │        │
┌──▼────┐ ┌─▼──────┐
│  DB   │ │ Redis  │
│ (PG)  │ │ Cache  │
└───────┘ └────────┘
```

## Démarrage rapide

### Prérequis

- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### Installation

1. **Cloner le repository**
```bash
git clone <votre-repo-url>
cd TPDocker1
```

2. **Configurer les variables d'environnement**
```bash
cp .env.example .env
# Éditer .env et définir POSTGRES_PASSWORD
```

3. **Lancer la stack**
```bash
docker compose up --build
```

4. **Accéder à l'application**
- Frontend : http://localhost:8080
- API : http://localhost:8000

## Tests de résilience

### Test 1 : Graceful degradation Redis

Vérifier que l'application continue de fonctionner si Redis est indisponible :

```bash
# Arrêter Redis
docker compose stop redis

# Vérifier que le dashboard fonctionne toujours
# → Les étudiants s'affichent avec "Vues: ?" au lieu d'un nombre

# Redémarrer Redis
docker compose start redis
```

### Test 2 : Persistance des données

Vérifier que les données survivent à un redémarrage complet :

```bash
# Arrêter tous les services
docker compose down

# Redémarrer
docker compose up -d

# → Les données Postgres et le compteur Redis sont conservés
```

## Structure du projet

```
.
├── docker-compose.yml          # Orchestration des services
├── python.Dockerfile           # Image API (non-root)
├── requirements.txt            # Dépendances Python
├── app/
│   └── main.py                # Code de l'API FastAPI
├── frontend/
│   └── index.html             # Interface SPA (immuable)
└── sqlfiles/
    ├── migration-v001.sql     # Table utilisateur
    └── migration-v002-students.sql  # Table students
```

## Sécurité

### Mesures implémentées

- **Non-root** : L'API tourne avec l'utilisateur `appuser` (UID 1000)
- **Isolation réseau** : 2 réseaux Docker séparés
  - `frontend_net` : communication frontend ↔ API
  - `backend_net` : communication API ↔ DB/Redis
- **Exposition minimale** : Seuls les ports 8080 et 8000 sont exposés
- **Secrets** : Mot de passe Postgres via variable d'environnement

## Services

### Frontend (Nginx)
- **Image** : `nginx:alpine`
- **Port** : 8080
- **Rôle** : Servir l'interface HTML statique

### API (FastAPI)
- **Image** : Custom (`python.Dockerfile`)
- **Port** : 8000
- **Rôle** : Logique métier, requêtes SQL, compteur Redis
- **Healthcheck** : Attend que DB et Redis soient prêts

### Database (Postgres)
- **Image** : `postgres:latest`
- **Volumes** : `pgdata` (persistance)
- **Init** : Scripts SQL auto-exécutés au premier démarrage
- **Healthcheck** : `pg_isready`

### Cache (Redis)
- **Image** : `redis:alpine`
- **Volumes** : `redisdata` (persistance AOF)
- **Mode** : Append-Only File activé
- **Healthcheck** : `redis-cli ping`

## Commandes utiles

```bash
# Voir les logs en temps réel
docker compose logs -f

# Voir les logs d'un service spécifique
docker compose logs -f api

# Reconstruire uniquement l'API
docker compose build api
docker compose up -d api

# Voir l'état des services
docker compose ps

# Nettoyer complètement (perte des données)
docker compose down -v

# Voir les réseaux Docker
docker network ls
```

## Fonctionnalités

### API Endpoints

- `GET /` : Liste des étudiants avec compteur de vues global

**Exemple de réponse :**
```json
[
  {
    "id": 1,
    "nom": "Zaher Madi",
    "promo": "M2 Dev 2526",
    "views": 42
  }
]
```

### Comportement

- Le compteur `views` s'incrémente à chaque requête
- Si Redis est down, `views` vaut `null` (graceful degradation)
- Les données sont rafraîchies automatiquement toutes les 5 secondes

## Troubleshooting

### Erreur "connection refused" sur l'API

```bash
# Vérifier que les services sont healthy
docker compose ps

# Si API restart en boucle, vérifier les logs
docker compose logs api
```

### Les scripts SQL ne s'exécutent pas

```bash
# Les scripts ne rejouent pas si la DB existe déjà
docker compose down -v  # Supprime les volumes
docker compose up --build
```

### Permission denied dans le conteneur API

```bash
# Vérifier que l'utilisateur appuser existe
docker compose exec api whoami
# → Doit retourner "appuser"
```

## Notes de développement

- Le frontend est **immuable** (ne pas modifier)
- L'API utilise `CORS: *` (à restreindre en production)
- Redis INCR est atomique (pas de race condition)
- Les healthchecks retardent le démarrage (normal)

## Licence

Projet éducatif - YNOV Copyright 2026

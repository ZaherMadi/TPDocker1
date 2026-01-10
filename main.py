import psycopg2
import os
import redis
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins= ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

# Connexion Postgres
conn = psycopg2.connect(
    host=os.getenv("POSTGRES_HOST"),
    port=5432,
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD"),
    database=os.getenv("POSTGRES_DB", "ynov_ci")
)

# Connexion Redis
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

@app.get('/')
async def get_students():
    # Récupération des étudiants depuis Postgres
    cur = conn.cursor()
    cur.execute("SELECT id, nom, promo FROM students;")
    rows = cur.fetchall()

    # Incrémenter le compteur de vues dans Redis
    try:
        views_count = redis_client.incr("page_views")
    except:
        # Graceful degradation: Si Redis est down, on continue sans le compteur
        views_count = None

    # Construction de la réponse
    students = []
    for row in rows:
        students.append({
            "id": row[0],
            "nom": row[1],
            "promo": row[2],
            "views": views_count
        })

    return students




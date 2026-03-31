from fastapi import FastAPI
import psycopg2

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        dbname="recommender_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

@app.get("/")
def home():
    return {"message": "Recommender API running 🚀"}

@app.get("/recommend")
def recommend(user_id: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT parent_asin, title, rating
        FROM recommendations
        WHERE user_id = %s
        ORDER BY rating DESC
        LIMIT 10
    """, (user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return {"recommendations": rows}
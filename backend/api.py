from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# ✅ CORS (keep this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_connection():
    return psycopg2.connect(
        dbname="recommender_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )
@app.get("/data")
def get_all_data():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            title_review,
            rating,
            review_text,
            user_id,
            review_year,
            review_month,
            store,
            categories
        FROM recommendations
    
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "title": r[0],
            "rating": r[1],
            "review_text": r[2],
            "user_id": r[3],
            "year": r[4],
            "month": r[5],
            "store": r[6],
            "categories": r[7],
        }
        for r in rows
    ]
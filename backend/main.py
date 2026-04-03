from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import psycopg2

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
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

@app.get("/")
def root():
    return {"message": "API is running 🚀"}

@app.get("/users")
def get_users():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT user_id
        FROM recommendations
        ORDER BY user_id
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"user_id": r[0]} for r in rows]


@app.get("/data/{user_id}")
def get_user_data(user_id: int):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            group_name,
            max_cosine,
            predicted_rating,
            display_label
        FROM recommendations
        WHERE user_id = %s
        LIMIT 5000
    """,(user_id,))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [
        {
            "group_name": r[0],
            "max_cosine": r[1],
            "predicted_rating": r[2],
            "display_label": r[3],
        }
        for r in rows
    ]
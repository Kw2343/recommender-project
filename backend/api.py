from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import math

app = FastAPI(title="Recommendation Dashboard API")

# CORS (required for Cloudflare dashboards)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_connection():
    return psycopg2.connect(
        dbname="recommender_db",
        user="postgres",
        password="1234",
        host="localhost",
        port="5432"
    )

# Convert NaN → None
def clean(v):
    if isinstance(v, float) and math.isnan(v):
        return None
    return v


# Root
@app.get("/")
def root():
    return {"message": "API running 🚀"}


# ============================
# SUMMARY (dashboard cards)
# ============================
@app.get("/summary")
def summary():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            COUNT(*) ,
            COUNT(DISTINCT parent_asin),
            COUNT(DISTINCT user_id),
            COUNT(DISTINCT CASE WHEN review_text IS NOT NULL THEN parent_asin END),
            COUNT(DISTINCT CASE WHEN review_text IS NULL THEN parent_asin END)
        FROM recommendations
    """)

    r = cur.fetchone()

    cur.close()
    conn.close()

    return {
        "total_reviews": r[0],
        "total_products": r[1],
        "unique_users": r[2],
        "products_with_reviews": r[3],
        "no_review_products": r[4]
    }


# ============================
# STORES FILTER
# ============================
@app.get("/stores")
def stores():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT store
        FROM recommendations
        WHERE store IS NOT NULL
        ORDER BY store
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return [{"store": r[0]} for r in rows]


# ============================
# MAIN DATA ENDPOINT
# ============================
@app.get("/data")
def data(
    limit: int = Query(5000),
    offset: int = Query(0),
    store: str | None = None,
    category: str | None = None,
    min_rating: float | None = None,
    max_rating: float | None = None
):

    if limit > 100000:
        limit = 100000

    conn = get_connection()
    cur = conn.cursor()

    query = """
        SELECT
            id,
            rating,
            title_review,
            review_text,
            user_id,
            parent_asin,
            price,
            store,
            categories,
            review_year,
            review_month,
            average_rating,
            rating_number
        FROM recommendations
        WHERE 1=1
    """

    params = []

    if store:
        query += " AND store = %s"
        params.append(store)

    if category:
        query += " AND categories ILIKE %s"
        params.append(f"%{category}%")

    if min_rating:
        query += " AND rating >= %s"
        params.append(min_rating)

    if max_rating:
        query += " AND rating <= %s"
        params.append(max_rating)

    query += " ORDER BY id LIMIT %s OFFSET %s"

    params.append(limit)
    params.append(offset)

    cur.execute(query, tuple(params))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    results = []

    for r in rows:

        results.append({
            "id": r[0],
            "rating": clean(r[1]),
            "title": r[2],
            "review_text": r[3],
            "user_id": r[4],
            "product_id": r[5],
            "price": clean(r[6]),
            "store": r[7],
            "category": r[8],
            "review_year": r[9],
            "review_month": r[10],
            "average_rating": clean(r[11]),
            "rating_number": clean(r[12])
        })

    return results
print("🚀 Starting ingestion...")

import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch

# ✅ LOAD DATA FIRST
df = pd.read_csv(r"C:\Users\user\recommender_project\backend\reviews_products_merged.csv")

print("✅ File loaded")
print("Rows:", len(df))
print("Columns:", df.columns)

conn = psycopg2.connect(
    dbname="recommender_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    rating FLOAT,
    title_review TEXT,
    review_text TEXT,
    user_id TEXT,
    parent_asin TEXT,
    price FLOAT,
    store TEXT,
    categories TEXT,
    review_year INT,
    review_month INT,
    average_rating FLOAT,
    rating_number INT
);
""")

records = [
    (
        row.get("rating"),
        row.get("title_review"),
        row.get("text"),
        row.get("user_id"),
        row.get("parent_asin"),
        row.get("price"),
        row.get("store"),
        str(row.get("categories")),
        row.get("review_year"),
        row.get("review_month"),
        row.get("average_rating"),
        row.get("rating_number")
    )
    for _, row in df.iterrows()
]

execute_batch(cur, """
INSERT INTO recommendations (
    rating, title_review, review_text, user_id, parent_asin,
    price, store, categories, review_year, review_month,
    average_rating, rating_number
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
""", records)

conn.commit()
cur.close()
conn.close()

print("🎉 Data inserted successfully")
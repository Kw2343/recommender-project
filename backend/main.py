import psycopg2
from psycopg2.extras import execute_batch
import pandas as pd

df = pd.read_csv(
    r"C:\Users\user\recommender_project\backend\merged_data.csv"
)

print("✅ Data loaded:", len(df))

print("📡 Connecting to DB...")

conn = psycopg2.connect(
    dbname="recommender_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

cur.execute("""
DROP TABLE IF EXISTS recommendations;

CREATE TABLE recommendations (
    id SERIAL PRIMARY KEY,
    parent_asin TEXT,
    title TEXT,
    rating FLOAT,
    review_text TEXT,
    user_id TEXT
);
""")

print("✅ Table ready")

# Prepare data (IMPORTANT: reduce columns!)
data = [
    (
        row.get("parent_asin"),
        row.get("title"),
        row.get("rating"),
        row.get("text"),
        row.get("user_id")
    )
    for _, row in df.iterrows()
]

print(f"📦 Inserting {len(data)} rows...")

execute_batch(cur, """
    INSERT INTO recommendations
    (parent_asin, title, rating, review_text, user_id)
    VALUES (%s, %s, %s, %s, %s)
""", data)

conn.commit()

cur.close()
conn.close()

print("🎉 DB INSERT COMPLETE")
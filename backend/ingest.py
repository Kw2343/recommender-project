import pandas as pd
import psycopg2

print("🚀 Starting ingestion...")

# Load Excel (you already confirmed this works)
df = pd.read_excel("backend/clean_meta_with_item.xlsx")

print("Columns:", df.columns)

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="recommender_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

# Create table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS recommendations (
    id SERIAL PRIMARY KEY,
    title TEXT,
    category TEXT
);
""")

# Insert data (simplified for now)
for i, row in df.iterrows():
    try:
        cur.execute("""
            INSERT INTO recommendations (title, category)
            VALUES (%s, %s)
        """, (
            row.get("title"),
            str(row.get("category"))
        ))
    except Exception as e:
        print(f"Row {i} failed:", e)

conn.commit()
cur.close()
conn.close()

print("✅ Data inserted successfully")
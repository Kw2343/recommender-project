from sqlalchemy import create_engine

# CHANGE password to your PostgreSQL password
DB_URL = "postgresql://postgres:password@localhost:5432/recommender_db"

engine = create_engine(DB_URL)
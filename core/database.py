from sqlalchemy import create_engine, MetaData, text
import os

# The 'DB_HOST' will be 'postgres' in Docker, and 'localhost' on your PC
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = "root"
DB_PASS = "root"
DB_NAME = "rec_engine_db"

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
metadata = MetaData()
with engine.begin() as conn:
    conn.execute(text("""
        CREATE TABLE IF NOT EXISTS interactions (
            user_id INT,
            item_id INT,
            interaction_score FLOAT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """))
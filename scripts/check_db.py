import os
from dotenv import load_dotenv
import psycopg

load_dotenv()

conn = psycopg.connect(
    host=os.environ["ROUNDS_DB_HOST"],
    port=os.environ["ROUNDS_DB_PORT"],
    dbname=os.environ["ROUNDS_DB_NAME"],
    user=os.environ["ROUNDS_DB_USERNAME"],
    password=os.environ["ROUNDS_DB_PASSWORD"]
)

with conn:
    rows = conn.execute("SELECT id, title FROM documents").fetchall()
    for id, title in rows:
        print(f"{id}: {title}")
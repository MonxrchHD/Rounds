import os
from dotenv import load_dotenv
import psycopg

from rounds.db import get_connection


with get_connection() as conn:
    rows = conn.execute("SELECT id, title FROM documents").fetchall()
    for id, title in rows:
        print(f"{id}: {title}")
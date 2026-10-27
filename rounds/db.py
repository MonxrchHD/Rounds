import os
from dotenv import load_dotenv
import psycopg

def get_connection():
    load_dotenv()

    return psycopg.connect(
        host=os.environ["ROUNDS_DB_HOST"],
        port=os.environ["ROUNDS_DB_PORT"],
        dbname=os.environ["ROUNDS_DB_NAME"],
        user=os.environ["ROUNDS_DB_USERNAME"],
        password=os.environ["ROUNDS_DB_PASSWORD"]
)

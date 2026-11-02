
from pgvector.psycopg import register_vector
import re

def search(conn, model, question, k = 5):
    register_vector(conn)
    question_vector = model.encode(question)

    rows = conn.execute(
        """
        SELECT chunks.id, chunks.content, chunks.start_page_number, chunks.end_page_number, documents.title, chunks.embedding <=> %s AS distance
        FROM chunks
        JOIN documents on documents.id = chunks.document_id
        WHERE documents.status = 'ready'
        ORDER BY distance
        LIMIT %s
        """,
        (question_vector, k),
    ).fetchall()

    return rows

def keyword_search(conn, question,  n = 20):
    words = re.findall(r"[a-z0-9]+", question.lower())
    if not words:
        return []
    or_query = " | ".join(words)
    return conn.execute(
        """
        SELECT chunks.id, chunks.content, chunks.start_page_number, chunks.end_page_number, documents.title, ts_rank(to_tsvector('english', chunks.content), to_tsquery('english', %s)) AS score
        FROM chunks
        JOIN documents ON documents.id = chunks.document_id
        WHERE to_tsvector('english', chunks.content) @@ to_tsquery('english', %s) AND documents.status = 'ready'
        ORDER BY score DESC
        LIMIT %s
        """,
        (or_query, or_query, n),
    ).fetchall()
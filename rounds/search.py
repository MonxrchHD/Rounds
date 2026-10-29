
from pgvector.psycopg import register_vector


def search(conn, model, question, k = 5):
    register_vector(conn)
    question_vector = model.encode(question)

    rows = conn.execute(
        """
        SELECT chunks.content, chunks.start_page_number, chunks.end_page_number, documents.title, chunks.embedding <=> %s AS distance
        FROM chunks
        JOIN documents on documents.id = chunks.document_id
        WHERE documents.status = 'ready'
        ORDER BY distance
        LIMIT %s
        """,
        (question_vector, k),
    ).fetchall()

    return rows

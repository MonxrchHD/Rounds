from pgvector.psycopg import register_vector


def save_chunks(conn, document_id, chunks, embeddings):
    register_vector(conn)
    rows = []
    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        text, start_page, end_page = chunk
        rows.append((document_id, i, text, start_page, end_page, embedding))
    conn.cursor().executemany(
            "INSERT INTO chunks (document_id, chunk_index, content, start_page_number, end_page_number, embedding) VALUES (%s, %s, %s, %s, %s, %s)",
            rows
        )
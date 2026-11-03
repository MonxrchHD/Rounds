from pgvector.psycopg import register_vector


def save_chunks(conn, document_id, chunks, embeddings, search_texts):
    register_vector(conn)
    rows = []
    for i, (chunk, embedding, search_text) in enumerate(zip(chunks, embeddings, search_texts)):
        text, start_page, end_page = chunk
        rows.append((document_id, i, text, start_page, end_page, embedding, search_text))
    conn.cursor().executemany(
            "INSERT INTO chunks (document_id, chunk_index, content, start_page_number, end_page_number, embedding, search_text) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            rows
        )

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

def fuse_rankings(result_lists, k = 60):
    scores ={}
    rows = {}

    for result_list in result_lists:
        for rank, entry in enumerate(result_list, start = 1):
            chunk_id = entry[0]
            scores[chunk_id] = scores.get(chunk_id,0) + 1/ (k + rank)
            if chunk_id not in rows:
                rows[chunk_id] = entry

    order = sorted(scores, key = scores.get, reverse = True)
    return [rows[r][:-1] + (scores[r],) for r in order]


def hybrid_search(conn, model, question, k = 5, pool = 20):
    embedding_results = search(conn, model, question, k = pool)
    keyword_results = keyword_search(conn, question, n = pool)
    fused_results = fuse_rankings([embedding_results, keyword_results])
    return fused_results[:k]

def chunks_for_pages(conn, start_page, end_page):
    return conn.execute(
        """
        SELECT chunks.id, chunks.content, chunks.start_page_number, chunks.end_page_number, documents.title, 0  AS score
        FROM chunks
        JOIN documents on documents.id = chunks.document_id
        WHERE chunks.start_page_number <= %s
          AND chunks.end_page_number >= %s
          AND documents.status = 'ready'
        ORDER BY chunks.chunk_index         
        """,
        (end_page, start_page),
    ).fetchall()
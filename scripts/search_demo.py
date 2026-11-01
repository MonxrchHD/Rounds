from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.search import search

model = load_model()
with get_connection() as conn:
    question = "What causes cotton-wool spots?"
    results = search(conn, model, question, k=5)
    for content, start_page, end_page, title, distance in results:
        print(f"Title: {title}, Pages: {start_page}-{end_page}, Distance: {round(distance, 3)}")
        print(f"Content: {content[:150]}\n")

SELECT chunks.chunk_index, chunks.start_page_number, chunks.end_page_number, ts_rank(to_tsvector('english', chunks.content), query) AS score
FROM chunks, plainto_tsquery('english', 'Which NPDR finding best predicts progression to proliferative diabetic retinopathy') AS query
WHERE to_tsvector('english', chunks.content) @@ query
ORDER BY score DESC
LIMIT 5; 
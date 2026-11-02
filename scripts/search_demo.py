from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.search import search

model = load_model()
with get_connection() as conn:
    question = "What causes cotton-wool spots?"
    results = search(conn, model, question, k=5)
    for chunk_id,content, start_page, end_page, title, distance in results:
        print(
            f"Title: {title}, Pages: {start_page}-{end_page}, Distance: {round(distance, 3)}")
        print(f"Content: {content[:150]}\n")

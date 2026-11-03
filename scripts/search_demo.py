from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.search import hybrid_search, keyword_search, search

QUESTION = "What causes cotton-wool spots?"
K = 5

model = load_model()


def show(label, results):
    print(f"=== {label} ===")
    for rank, (chunk_id, content, start_page, end_page, title, score) in enumerate(results, start=1):
        print(f"{rank}. pages {start_page}-{end_page} | score {score:.4f} | {content[:100]}")
    print()


with get_connection() as conn:
    show("Embedding only", search(conn, model, QUESTION, k=K))
    show("Keyword only", keyword_search(conn, QUESTION, n=K))
    show("Hybrid", hybrid_search(conn, model, QUESTION, k=K))
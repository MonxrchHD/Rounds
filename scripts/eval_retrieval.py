import json

from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.evaluation import first_hit_rank, retrieval_metrics
from rounds.search import hybrid_search

FILE_PATH = ["evals/golden_cases.json", "evals/retrieval_cases.json"]
K = 5

cases = []
for path in FILE_PATH:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    cases.extend(data["cases"])

cases = [case for case in cases if case["expected_viewer_pages"] is not None]
model = load_model()
ranks = []
with get_connection() as conn:
    for case in cases:
        pages = case["expected_viewer_pages"]
        results = hybrid_search(conn, model, case["retrieval_query"], k=K)
        rank = first_hit_rank(results, pages["start"], pages["end"])
        ranks.append(rank)
        print(f"{case['id']:<10} {'MISS' if rank is None else f'Rank: {rank}'}")

hit_rate, mrr = retrieval_metrics(ranks)
print(f"\n{len(cases)} cases | hit rate @ {K}: {hit_rate:.2f} | MRR: {mrr:.3f}")
  


def pages_overlap(chunk_start, chunk_end, exp_start, exp_end):
    return chunk_start <= exp_end and chunk_end >= exp_start

def first_hit_rank(results, exp_start, exp_end):
    for rank, (content, start_page, end_page, title, distance) in enumerate(results, start=1):
        if pages_overlap(start_page, end_page, exp_start, exp_end):
            return rank
    return None

def retrieval_metrics(ranks):
    hits = [rank for rank in ranks if rank is not None]
    hit_rate = len(hits) / len(ranks) if ranks else 0
    mrr = sum(1 / rank for rank in hits) / len(ranks) if ranks else 0
    return hit_rate, mrr
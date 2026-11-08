import pytest

from rounds.search import fuse_rankings
from rounds.db import get_connection
from rounds.evaluation import pages_overlap
from rounds.search import chunks_for_pages

# Fake rows: (chunk_id, filler, original_score)
# Only the id (first value) and the last value matter to fuse_rankings.
EMBEDDING = [(30, "x", 0.2), (12, "x", 0.3), (9, "x", 0.4), (41, "x", 0.5), (7, "x", 0.6)]
KEYWORD = [(9, "x", 0.9), (8, "x", 0.8), (22, "x", 0.7), (30, "x", 0.6), (0, "x", 0.5)]


def test_fused_order_matches_hand_calculation():
    fused = fuse_rankings([EMBEDDING, KEYWORD])
    ids = [row[0] for row in fused]
    assert ids[:3] == [9, 30, 12]


def test_fused_score_replaces_original_score():
    fused = fuse_rankings([EMBEDDING, KEYWORD])
    top_score = fused[0][-1]
    assert top_score == pytest.approx(1 / 61 + 1 / 63)


def test_chunk_in_both_lists_beats_chunk_in_one():
    fused = fuse_rankings([EMBEDDING, KEYWORD])
    ids = [row[0] for row in fused]
    # Chunk 41 is 4th in embeddings only; chunk 30 is in both lists.
    assert ids.index(30) < ids.index(41)


def test_every_chunk_appears_once():
    fused = fuse_rankings([EMBEDDING, KEYWORD])
    ids = [row[0] for row in fused]
    assert len(ids) == len(set(ids))
    assert set(ids) == {30, 12, 9, 41, 7, 8, 22, 0}

def test_chunks_for_pages_returns_overlapping_chunks():
    with get_connection() as conn:
        results = chunks_for_pages(conn, 17, 17)
    assert results
    for _chunk_id, _content, start_page, end_page, _title, _score in results:
        assert pages_overlap(start_page, end_page, 17, 17)


def test_chunks_for_pages_outside_ingested_range_is_empty():
    with get_connection() as conn:
        results = chunks_for_pages(conn, 1, 5)
    assert results == []


def test_chunks_for_pages_rows_have_six_fields():
    with get_connection() as conn:
        results = chunks_for_pages(conn, 17, 17)
    assert all(len(row) == 6 for row in results)
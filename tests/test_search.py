import pytest

from rounds.search import fuse_rankings

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
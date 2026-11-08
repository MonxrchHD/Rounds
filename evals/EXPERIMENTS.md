# Retrieval Experiments

Results from `python -m scripts.eval_retrieval` on the `evals/retina-atlas` golden set.

- **Dataset:** Diagnostic Atlas of Retinal Diseases, Volume 1 (viewer pages 15–290)
- **Cases scored:** 35 (10 golden cases + 25 retrieval-only cases; `oos-01` excluded)- **Metrics:** hit rate @ 5 (share of cases with a correct chunk in the top 5) and MRR (mean of 1/rank, 0 for a miss). Higher is better for both.
- **Hit rule:** a returned chunk counts as correct if its page range overlaps the case's `expected_viewer_pages`.
- **Caution:** with 10 cases, one case changes hit rate by 0.10. Treat small differences as directional, not conclusive.
- **Decision rule:** a change ships only if hit rate @ 5 rises; MRR breaks ties. The tutor reads all top 5 results, so finding a correct chunk matters more than its exact position.

## Results log

| Date | Change | Hit@5 | MRR | Notes |
|---|---|---|---|---|
| 2026-10-31 | Embedding search (baseline): all-MiniLM-L6-v2, cosine distance, 245-token chunks, 40-token overlap | 0.80 | 0.720 | Misses: npdr-04, npdr-06. npdr-03 at rank 5. |
| 2026-11-01 | + Hybrid search: keyword search (Postgres full-text, OR matching) fused with embeddings via Reciprocal Rank Fusion (k=60, pool=20) | 0.90 | 0.820 | npdr-03 5 → 1; npdr-06 miss → 5. Nothing got worse. |
| 2026-11-02 | + Abbreviation expansion in `search_text`, used by both embeddings and keyword search | 0.80 | 0.750 | Regression. Expanding common abbreviations (DR, NPDR, PDR) inserted "diabetic retinopathy" into most chunks, so OR keyword matching stopped distinguishing them. npdr-06 5 → miss; npdr-07 1 → 2. npdr-04 still a miss. |
| 2026-11-02 | Abbreviation expansion for embeddings only (keyword search back on `content`) | 0.90 | 0.783 | npdr-06 recovered to rank 3. Embeddings now rank the CWS chunk 4th for npdr-04, but fusion pushes it out. npdr-07 stays at 2, likely because measuring expanded text shifts chunk boundaries. |
| 2026-11-02 | **Shipped:** expansion behind `EXPAND_ABBREVIATIONS = False` | **0.90** | **0.820** | Reproduces the hybrid result exactly, confirming the flag restores prior behavior. |
| 2026-11-02 | Grew eval set from 10 to 35 cases (25 retrieval-only cases from chapters 1–5); config unchanged (hybrid, expansion off) | 0.86 | 0.714 | New baseline. Lower than 0.90 partly because the original 10 had been used to tune the system. Misses: npdr-04, r-pdr-03, r-pdr-05, r-dme-07, r-brvo-03. All five involve a term the student types in full that the source mostly abbreviates (CWS, PDR, PRP, CSME, BRVO). |
| 2026-11-02 | Abbreviation expansion on 35 cases (embeddings use expanded text, keyword search on `content`) | 0.86 | 0.677 | Not shipped: same hit rate, lower MRR. Fixed r-pdr-05 (miss → 5) and r-dme-07 (miss → 3), both abbreviation cases. Broke r-dme-05 (1 → miss) and r-brvo-02 (5 → miss), neither an abbreviation case, likely from shifted chunk boundaries. Rule set beforehand: ship only if hit rate rises. |
| 2026-11-07 | prompt-v1, gold context (search for out-of-scope), claude-sonnet-5-5 | 9/11 | Fails: npdr-05 (no prompt toward IRMA or the quadrant count), oos-01 (gave away the pending question's answer). Run: `evals/runs/2026-11-07_prompt-v1.json` |

## Current configuration (shipped)

| Setting | Value |
|---|---|
| Embedding model | `all-MiniLM-L6-v2` (384 dimensions) |
| Chunk size / overlap | 245 / 40 tokens, sentence-aligned |
| Search | Hybrid: embeddings + keyword, RRF k=60, pool=20, top 5 |
| Keyword search reads | `chunks.content` |
| **Abbreviation expansion:** on 35 cases it fixes abbreviation misses but shifts chunk boundaries, which breaks others. Next experiment: keep chunk boundaries from the original text and expand only the embedded text, with a safety margin so the expanded text stays under the 254-token limit. |

## Open questions

- **npdr-04** ("What causes cotton-wool spots?"): the answer chunk uses only the abbreviation "CWS." Expansion helps embeddings, but not yet enough to reach the top 5 after fusion.
- **Abbreviation expansion:** re-test once the golden set reaches 30–50 cases. Ideas to try: expand only rare abbreviations, or expand only the first occurrence per chunk.
- **Chunk boundaries:** measuring tokens on expanded text changes how sentences group into chunks, which may explain npdr-07's drop. Consider sizing chunks on original text with a safety margin instead.
- **Eval size:** grow from 10 to 30–50 cases so differences between versions are meaningful.
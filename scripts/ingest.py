from pypdf import PdfReader
from rounds.chunking import build_chunks, is_quality_sentence, filter_page_range, is_reference_sentence, split_document
from rounds.cleaning import clean_pages, find_abbreviations, expand_abbreviations
from rounds.db import get_connection
from rounds.embedding import embed_texts, load_model
from rounds.storage import save_chunks


DOCUMENT_ID = 1
PDF_PATH = "data/atlas_vol1.pdf"
PAGE_RANGE = (15, 290)
EXPAND_ABBREVIATIONS = False
model = load_model()




reader = PdfReader(PDF_PATH)
page_texts = [page.extract_text() for page in reader.pages]

pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)
whole_text = "\n".join(pages)
if EXPAND_ABBREVIATIONS:
    abbreviations = find_abbreviations(whole_text)
else:
    abbreviations = {}

def count_tokens(text):
    return len(model.tokenizer.tokenize(expand_abbreviations(text, abbreviations)))

sentences = split_document(pages)

good = [s for s in sentences if is_quality_sentence(
    s[0]) and not is_reference_sentence(s[0])]
in_range = filter_page_range(good, PAGE_RANGE[0], PAGE_RANGE[1])
chunks = build_chunks(in_range, count_tokens)
search_texts = [expand_abbreviations(text, abbreviations) for text, start, end in chunks]
assert max(len(model.tokenizer.tokenize(t)) for t in search_texts) <= 254
embeddings = embed_texts(search_texts, model)

with get_connection() as conn:
    conn.execute("DELETE FROM chunks WHERE document_id = %s", (DOCUMENT_ID,))
    save_chunks(conn, DOCUMENT_ID, chunks, embeddings, search_texts)
    conn.execute(
        "UPDATE documents SET status = %s, updated_at = now() WHERE id = %s", ("ready", DOCUMENT_ID))


print(f"Saved {len(chunks)} chunks for document {DOCUMENT_ID} with embeddings of shape {embeddings.shape}.")

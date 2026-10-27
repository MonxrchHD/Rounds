from pypdf import PdfReader
from rounds.cleaning import clean_pages
from rounds.chunking import build_chunks, filter_page_range, is_reference_sentence, split_document, is_quality_sentence, count_tokens, split_long_sentence
from sentence_transformers import SentenceTransformer

from rounds.embeddings import embed_texts, load_model

model = load_model()
reader = PdfReader("data/atlas_vol1.pdf")
page_texts = [page.extract_text() for page in reader.pages]

pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)

sentences = split_document(pages)

good = [s for s in sentences if is_quality_sentence(s[0]) and not is_reference_sentence(s[0])]
in_range = filter_page_range(good, 15, 290)
chunks = build_chunks(in_range, count_tokens)

assert max(count_tokens(text) for text, start, end in chunks) <= 254

embeddings = embed_texts([text for text, start, end in chunks], model)
print(embeddings.shape)
print(len(chunks))
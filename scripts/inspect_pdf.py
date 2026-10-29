from pypdf import PdfReader
from rounds.cleaning import clean_pages
from rounds.chunking import build_chunks, filter_page_range, is_reference_sentence, split_document, is_quality_sentence, split_long_sentence
from sentence_transformers import SentenceTransformer

from rounds.embedding import embed_texts, load_model

model = load_model()
reader = PdfReader("data/atlas_vol1.pdf")
page_texts = [page.extract_text() for page in reader.pages]


def count_tokens(text):
    return len(model.tokenizer.tokenize(text))


pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)

sentences = split_document(pages)
for text, start, end in sentences:
    if "Diabetic retinopathy (DR)" in text:
        print(start, end, "|", text)

from pypdf import PdfReader
from rounds.cleaning import clean_pages
from rounds.chunking import build_chunks, filter_page_range, is_reference_sentence, split_document, is_quality_sentence, count_tokens, split_long_sentence
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
reader = PdfReader("data/atlas_vol1.pdf")
page_texts = [page.extract_text() for page in reader.pages]

pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)

sentences = split_document(pages)

good = [s for s in sentences if is_quality_sentence(s[0]) and not is_reference_sentence(s[0])]
in_range = filter_page_range(good, 15, 290)
chunks = build_chunks(in_range, count_tokens)

counts = [(len(model.tokenizer.tokenize(text)), start, end) for text, start, end in chunks]
overflow = sum(1 for count, start, end in counts if count > 254)
print(max(counts))
print("Overflow chunks:", overflow)
worst = max(counts)
for text, start, end in chunks:
    if (start, end) == (worst[1], worst[2]):
        print(text)
        print(model.tokenizer.tokenize(text)[:60])
over = [(count, s, e) for count, s, e in counts if count > 254]
for count, s, e in over[:10]:
    for text, start, end in chunks:
        if (start, end) == (s, e):
            print(count, "|", text[:120])
            break
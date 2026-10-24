from pypdf import PdfReader
from rounds.cleaning import clean_pages
from rounds.chunking import build_chunks, filter_page_range, split_document, is_quality_sentence

reader = PdfReader("data/atlas_vol1.pdf")
page_texts = [page.extract_text() for page in reader.pages]

pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)

sentences = split_document(pages)

good = [s for s in sentences if is_quality_sentence(s[0])]
in_range = filter_page_range(good, 15, 290)
chunks = build_chunks(in_range)
print("Chunks:", len(chunks))
print("Largest chunk (words):", max(len(c[0].split()) for c in chunks))

for text, start, end in chunks[:2]:
    print(f"\n[{start}-{end}] {text}")
print("In range:", len(in_range))
print("Before:", len(sentences), "After:", len(good))

spanning = [s for s in good if s[1] != s[2]]
print("Spanning pages:", len(spanning))
for text, start, end in spanning[:3]:
    print(f"[{start}-{end}] {text}")

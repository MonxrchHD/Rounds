from pypdf import PdfReader
from rounds.cleaning import clean_pages
from rounds.chunking import filter_page_range, split_document, is_quality_sentence

reader = PdfReader("data/atlas_vol1.pdf")
page_texts = [page.extract_text() for page in reader.pages]

pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)

sentences = split_document(pages)

good = [s for s in in_range if is_quality_sentence(s[0])]
in_range = filter_page_range(good, 15, 290)
print("In range:", len(in_range))
print("Before:", len(sentences), "After:", len(good))

spanning = [s for s in good if s[1] != s[2]]
print("Spanning pages:", len(spanning))
for text, start, end in spanning[:3]:
    print(f"[{start}-{end}] {text}")

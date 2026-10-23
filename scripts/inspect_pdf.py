from pypdf import PdfReader
from rounds.cleaning import clean_pages, edge_lines, find_repeated_lines, rejoin_hyphenated_words, remove_repeated_lines, collapse_spaces, build_vocabulary

reader = PdfReader("data/atlas_vol1.pdf")
print("Total pages:", len(reader.pages))


first = 14
for index, page in enumerate(reader.pages[first:first + 5], start=first + 1):
    text = page.extract_text()
    print(f"Pdf viewer page {index}:\n{text[-200:]}\n")

page_texts = [page.extract_text() for page in reader.pages]
pages = clean_pages(page_texts)
assert len(pages) == len(page_texts)
print(pages[18][:400])
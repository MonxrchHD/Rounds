from pypdf import PdfReader
from rounds.cleaning import edge_lines, find_repeated_lines, rejoin_hyphenated_words, remove_repeated_lines, collapse_spaces, build_vocabulary

reader = PdfReader("data/atlas_vol1.pdf")
print("Total pages:", len(reader.pages))


first = 14
for index, page in enumerate(reader.pages[first:first + 5], start=first + 1):
    text = page.extract_text()
    print(f"Pdf viewer page {index}:\n{text[-200:]}\n")

page_texts = [page.extract_text() for page in reader.pages]
headers, footers = edge_lines(page_texts)
repeated = find_repeated_lines(headers + footers)
cleaned = remove_repeated_lines(page_texts, repeated)
assert len(cleaned) == len(page_texts)

final = [collapse_spaces(text) for text in cleaned]
vocab = build_vocabulary(final)
rejoined = [rejoin_hyphenated_words(text, vocab) for text in final]
assert len(rejoined) == len(page_texts)
print(rejoined[18][:400])
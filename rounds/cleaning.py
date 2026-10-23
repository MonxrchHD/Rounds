import re
from collections import Counter

HEADER_MIN_REPEATS = 3


def edge_lines(page_texts):
    headers = []
    footers = []
    for page_text in page_texts:
        lines = page_text.splitlines()
        stripped = [line.strip() for line in lines if line.strip()]
        if len(stripped) < 2:
            continue
        headers.append(stripped[0])
        footers.append(stripped[-1])
    return headers, footers


def find_repeated_lines(lines, min_repeats=HEADER_MIN_REPEATS):
    normalized = (normalize_line(line) for line in lines)

    counts = Counter(normalized)
    repeated = {line for line, count in counts.items() if count >= min_repeats}
    return repeated

def normalize_line(line):
    return re.sub(r"\d", "", line).strip()

def remove_repeated_lines(page_texts, repeated):
    cleaned_texts = []
    for page_text in page_texts:
        lines = [line.strip() for line in page_text.splitlines() if line.strip()]
        if lines and normalize_line(lines[0]) in repeated:
            lines = lines[1:]
        if lines and normalize_line(lines[-1]) in repeated:
            lines = lines[:-1]
        cleaned_texts.append("\n".join(lines))
    return cleaned_texts

def collapse_spaces(text):
    return re.sub(r" +", " ", text).strip()


def build_vocabulary(page_texts):
    words = set()
    for text in page_texts:
        words.update(re.findall(r"[a-z]+(?:-[a-z]+)*", text.lower()))

    return words

def rejoin_hyphenated_words(text, vocab):
    def replace_hyphenated(match):
        first = match.group(1)
        second = match.group(2)
        joined = first + second
        if joined.lower() in vocab:
            return joined
        else: 
            return first + "-" + second
    return re.sub(r"([A-Za-z]+)-\n([A-Za-z]+)", replace_hyphenated, text)

def clean_pages(page_texts):
    headers, footers = edge_lines(page_texts)
    repeated = find_repeated_lines(headers + footers)
    cleaned = remove_repeated_lines(page_texts, repeated)
    collapsed = [collapse_spaces(text) for text in cleaned]
    vocab = build_vocabulary(collapsed)
    rejoined = [rejoin_hyphenated_words(text, vocab) for text in collapsed]
    return rejoined
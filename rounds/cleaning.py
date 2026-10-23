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
    normalized = normalize_line(line) for line in lines

    counts = Counter(normalized)
    repeated = {line for line, count in counts.items() if count >= min_repeats}
    return repeated

def normalize_line(line):
    return re.sub(r"\d", "", line).strip()
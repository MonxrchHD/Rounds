HEADER_MIN_REPEATS = 5


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
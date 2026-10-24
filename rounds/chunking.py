import re


MIN_LOWERCASE_RATIO = 0.2
CHUNK_WORDS = 150
OVERLAP_WORDS = 20

def split_sentences(text):
    text = text.replace("\n", " ")
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def split_document(pages):
    results = []
    carry = ""
    carry_start = None



    for page_number, page in enumerate(pages, start = 1):
        if carry:
            page = carry + " " + page
            first_page = carry_start
        else:
            first_page = page_number
        sentences = split_sentences(page)
        if not sentences:
            continue
        for i, sentence in enumerate(sentences[:-1]):
            start = first_page if i == 0 else page_number
            results.append((sentence, start, page_number))

        last = sentences[-1]
        last_page = first_page if len(sentences) == 1 else page_number
        if last.endswith((".", "!", "?")):
            results.append((last, last_page, page_number))
            carry, carry_start = "", None
        else:
            carry, carry_start = last, last_page

    if carry:
        results.append((carry, carry_start, len(pages)))
    return results

def is_quality_sentence(sentence):
    non_space = sum(1 for c in sentence if not c.isspace())
    lower_case = sum(1 for c in sentence if c.islower())
    lowercase_ratio= lower_case/ non_space if non_space > 0 else 0
    return  lowercase_ratio >= MIN_LOWERCASE_RATIO 

def is_reference_sentence(text):
    names = r"[A-Z][a-z]+ [A-Z]{1,3},"
    tags = r"doi:|https?://|www\.|arxiv:|PMID:|PMC\d+"
    return len(re.findall(names, text)) >= 2 or len(re.findall(tags, text)) > 0

def filter_page_range(sentences, first_page, last_page):
    in_range = [s for s in sentences if first_page <= s[1] and s[2] <= last_page]
    return in_range

def make_chunk(sentences_in_chunk):
                chunk_text = " ".join(s[0] for s in sentences_in_chunk)
                chunk_start = sentences_in_chunk[0][1]
                chunk_end = sentences_in_chunk[-1][2]
                return (chunk_text, chunk_start, chunk_end)

def build_chunks(sentences):
    chunks = []
    current_chunk = []
    current_words = 0
    new_count = 0

    for text, start, end in sentences:
        words = text.split()
        if len(words) > CHUNK_WORDS:
            if new_count > 0:
                chunks.append(make_chunk(current_chunk))
            current_chunk = []
            current_words = 0
            new_count = 0
            for i in range(0, len(words), CHUNK_WORDS):
                chunk_text = " ".join(words[i:i + CHUNK_WORDS])
                chunks.append((chunk_text, start, end))
            continue
        if current_words + len(words) > CHUNK_WORDS:
            if new_count > 0:
                chunks.append(make_chunk(current_chunk))
            overlap = []
            overlap_words = 0
            for sentence in reversed(current_chunk):
                n = len(sentence[0].split())
                if overlap_words + n > OVERLAP_WORDS or overlap_words + len(words) + n > CHUNK_WORDS:
                    break
                overlap.insert(0, sentence)
                overlap_words += n
            current_chunk = overlap 
            current_words = overlap_words 
            new_count = 0
        current_chunk.append((text, start, end))
        current_words += len(words)
        new_count += 1
    if new_count > 0:
        chunks.append(make_chunk(current_chunk))
    return chunks
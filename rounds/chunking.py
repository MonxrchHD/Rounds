import re
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
MIN_LOWERCASE_RATIO = 0.2
CHUNK_TOKENS = 245
OVERLAP_TOKENS = 40

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

def count_tokens(text):
    tokens = model.tokenizer.tokenize(text)
    return len(tokens)

def split_long_sentence(text, count_tokens):
    words = text.split()
    chunk = []
    chunks = []
    token_count = 0
    for word in words:
        tokens = count_tokens(word)
        if chunk and token_count + tokens > CHUNK_TOKENS:
            chunks.append(" ".join(chunk))
            chunk = []
            token_count = 0
        chunk.append(word)
        token_count += tokens
    if chunk:
        chunks.append(" ".join(chunk))
    return chunks
        
def build_chunks(sentences, count_tokens):
    chunks = []
    current_chunk = []
    current_tokens = 0
    new_count = 0

    for text, start, end in sentences:
        pieces = count_tokens(text)
        if pieces > CHUNK_TOKENS:
            if new_count > 0:
                chunks.append(make_chunk(current_chunk))
            current_chunk = []
            current_tokens = 0
            new_count = 0
            for piece_text in split_long_sentence(text, count_tokens):
                chunks.append((piece_text, start, end))
            continue
        if current_tokens + pieces > CHUNK_TOKENS:
            if new_count > 0:
                chunks.append(make_chunk(current_chunk))
            overlap = []
            overlap_tokens = 0
            for sentence in reversed(current_chunk):
                n = count_tokens(sentence[0])
                if overlap_tokens + n > OVERLAP_TOKENS or overlap_tokens + pieces + n > CHUNK_TOKENS:
                    break
                overlap.insert(0, sentence)
                overlap_tokens += n
            current_chunk = overlap 
            current_tokens = overlap_tokens 
            new_count = 0
        current_chunk.append((text, start, end))
        current_tokens += pieces
        new_count += 1
    if new_count > 0:
        chunks.append(make_chunk(current_chunk))
    return chunks
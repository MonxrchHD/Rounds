import re


MIN_LOWERCASE_RATIO = 0.2

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

def filter_page_range(sentences, first_page, last_page):
    in_range = [s for s in sentences if first_page <= s[1] and s[2] <= last_page]
    return in_range

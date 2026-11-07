from pathlib import Path

from rounds.search import hybrid_search

MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 1000

SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "tutor_system.md"


def load_system_prompt():
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def format_sources(results):
    blocks = []
    for _chunk_id, content, start_page, end_page, title, _rrf_score in results:
        page_range = f"{start_page}-{end_page}" if start_page != end_page else f"{start_page}"
        blocks.append(f'<source title="{title}" pages="{page_range}">\n{content}\n</source>')
    return "\n\n".join(blocks)


def extract_text(response):
    texts = [block.text for block in response.content if block.type == "text"]
    if not texts:
        raise ValueError("No text block in response")
    return "\n\n".join(texts)


def tutor_turn(student_message, tutor_question, conn, embed_model, client):
    query = student_message + "\n\n" + tutor_question
    results = hybrid_search(conn, embed_model, query)
    content = "\n\n".join([
        format_sources(results),
        f"<tutor_question>\n{tutor_question}\n</tutor_question>",
        f"<student_message>\n{student_message}\n</student_message>",
    ])
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=load_system_prompt(),
        messages=[{"role": "user", "content": content}],
    )
    return extract_text(response), results
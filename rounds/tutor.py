from pathlib import Path

from rounds.search import hybrid_search

MODEL = "claude-sonnet-5-5"
MAX_TOKENS = 1000
OPENING_MESSAGE = "Start the session."
SYSTEM_PROMPT_PATH = Path(__file__).parent / "prompts" / "tutor_system.md"


def load_system_prompt():
    return SYSTEM_PROMPT_PATH.read_text(encoding="utf-8")


def format_sources(results):
    blocks = []
    for _chunk_id, content, start_page, end_page, title, _rrf_score in results:
        page_range = f"{start_page}-{end_page}" if start_page != end_page else f"{start_page}"
        blocks.append(
            f'<source title="{title}" pages="{page_range}">\n{content}\n</source>')
    return "\n\n".join(blocks)


def extract_text(response):
    texts = [block.text for block in response.content if block.type == "text"]
    if not texts:
        raise ValueError("No text block in response")
    return "\n\n".join(texts)


def tutor_turn(student_message, history, conn, embed_model, client):
    query = student_message + "\n\n" + history[-1]["content"]
    results = hybrid_search(conn, embed_model, query)
    reply = generate_reply(student_message, history, results, client)
    return reply, results


def generate_reply(student_message, history, results, client):
    messages = build_messages(history, student_message, results)
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=load_system_prompt(),
        messages= messages,
    )
    return extract_text(response)

def build_messages(history, student_message, results):
    content = "\n\n".join([
        format_sources(results),
        f"<student_message>\n{student_message}\n</student_message>",
    ])
    new_messages = {"role": "user", "content": content }
    return history + [new_messages]
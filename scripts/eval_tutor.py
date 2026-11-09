import json
import anthropic
from dotenv import load_dotenv
from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.search import chunks_for_pages, hybrid_search
from rounds.tutor import generate_reply
from pathlib import Path

RUN_NAME = "2026-11-08_prompt-v2"
RUNS_DIR = Path("evals/runs")
RUNS_DIR.mkdir(parents=True, exist_ok=True)
CASES_PATH = "evals/golden_cases.json"
CASE_ID = None


load_dotenv()

with open(CASES_PATH, encoding="utf-8") as f:
    data = json.load(f)

embed_model = load_model()
client = anthropic.Anthropic()

cases = data["cases"]
if CASE_ID:
    cases = [case for case in cases if case["id"] == CASE_ID]

records = []

with get_connection() as conn:
    for case in cases:
        student = case["student_answer"]
        tutor = case["tutor_question"]

        if case["expected_viewer_pages"] is not None:
            start, end = case["expected_viewer_pages"]["start"], case["expected_viewer_pages"]["end"]
            result = chunks_for_pages(conn, start, end)
            context = "gold"
        else:
            question = student + "\n\n" + tutor
            result = hybrid_search(conn, embed_model, question)
            context = "search"
        reply = generate_reply(student, tutor, result, client)
        pages = [
            (start_page, end_page)
            for _chunk_id, _content, start_page, end_page, _title, _score in result
        ]

        records.append({
            "id": case["id"],
            "reply": reply,
            "pages": pages,
            "student answer": student,
            "tutor question": tutor,
            "context": context,
        })

with open(RUNS_DIR / f"{RUN_NAME}.json", "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2)

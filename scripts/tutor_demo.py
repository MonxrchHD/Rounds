import json

import anthropic
from dotenv import load_dotenv

from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.tutor import tutor_turn

CASES_PATH = "evals/golden_cases.json"
CASE_ID = "npdr-04"

# 1. Load .env first, so ANTHROPIC_API_KEY exists before the client is created
load_dotenv()

# 2. Load the case
with open(CASES_PATH, encoding="utf-8") as f:
    data = json.load(f)
cases_by_id = {case["id"]: case for case in data["cases"]}
case = cases_by_id[CASE_ID]

# 3. Set up what tutor_turn needs
embed_model = load_model()
client = anthropic.Anthropic()

# 4. Run one tutor turn
with get_connection() as conn:
    reply, results = tutor_turn(case["student_answer"], case["tutor_question"], conn, embed_model, client)

print("RETRIEVED PAGES:")
for _chunk_id, _content, start_page, end_page, title, score in results:
    print(f"  {start_page}-{end_page}  (score {score:.4f})")
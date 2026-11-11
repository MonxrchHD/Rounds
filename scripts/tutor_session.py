import anthropic
from rounds.db import get_connection
from rounds.embedding import load_model
from rounds.tutor import tutor_turn, OPENING_MESSAGE
from dotenv import load_dotenv

load_dotenv()
client = anthropic.Anthropic()

FIRST_QUESTION = "What is the earliest hallmark lesion of diabetic retinopathy, and what goes wrong in the capillary to produce it?"
history = [{"role": "user", "content": OPENING_MESSAGE},
           {"role": "assistant", "content": FIRST_QUESTION}]
embed_model = load_model()
print(f"bot:", FIRST_QUESTION)
with get_connection() as conn:

    while True:
        text = input("You: ").strip()
        if text == "":
            print("Bot: I did not quite catch that.\n")
            continue
        if text.lower() == "quit":
            break
        reply, _result = tutor_turn(text, history, conn, embed_model, client)
        print("Bot: ", reply)
        history.append({"role": "user", "content": text})
        history.append({"role": "assistant", "content": reply})
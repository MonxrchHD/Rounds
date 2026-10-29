from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
print(model.max_seq_length)
tokens = model.tokenizer.tokenize("microaneurysms and hyperfluorescent points")
print(tokens)
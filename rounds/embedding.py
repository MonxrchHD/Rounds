from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"


def load_model():
    model = SentenceTransformer(MODEL_NAME)
    return model

def embed_texts(texts, model):
    return model.encode(texts, show_progress_bar=True)
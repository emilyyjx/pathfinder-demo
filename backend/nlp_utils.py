import spacy
from sentence_transformers import SentenceTransformer, util

nlp = spacy.load("en_core_web_sm")
model = SentenceTransformer("all-MiniLM-L6-v2")

def extract_keywords(text):
    doc = nlp(text)
    return [token.text.lower() for token in doc if token.pos_ in {"NOUN", "PROPN"}]

def compute_similarity(query, options):
    embeddings = model.encode([query] + options)
    scores = util.cos_sim(embeddings[0], embeddings[1:])[0]
    return sorted(zip(options, scores), key=lambda x: x[1], reverse=True)

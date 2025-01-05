import spacy

def load_model():
    nlp = spacy.load("en_core_web_sm")
    return nlp

def tokenize_text(text):
    nlp = load_model()
    doc = nlp(text)
    return [token.text for token in doc]

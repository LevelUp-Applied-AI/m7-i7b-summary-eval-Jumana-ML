import re
import string
from transformers import pipeline

def get_qa_model_name() -> str:
    """Return the default QA model name."""
    return "distilbert-base-cased-distilled-squad"

def build_qa_pipeline(model_name: str):
    """Build the Hugging Face QA pipeline."""
    return pipeline("question-answering", model=model_name)

def normalize_answer(s: str) -> str:
    """Lowercasing, removing punctuation and articles."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def exact_match(prediction: str, truth: str) -> int:
    """Compute Exact Match score."""
    return int(normalize_answer(prediction) == normalize_answer(truth))

def token_f1(prediction: str, truth: str) -> float:
    """Compute Token-level F1 score."""
    pred_tokens = normalize_answer(prediction).split()
    truth_tokens = normalize_answer(truth).split()
    if len(pred_tokens) == 0 or len(truth_tokens) == 0:
        return float(int(pred_tokens == truth_tokens))
    
    common = set(pred_tokens) & set(truth_tokens)
    if len(common) == 0:
        return 0.0
    
    precision = len(common) / len(pred_tokens)
    recall = len(common) / len(truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1

def predict_one(qa, question: str, context: str) -> dict:
    """Run inference using the QA pipeline."""
    return qa(question=question, context=context)
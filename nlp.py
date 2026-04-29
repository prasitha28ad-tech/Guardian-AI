import spacy
import re

# Load small english model for NER (Requires: python -m spacy download en_core_web_sm)
try:
    nlp_spacy = spacy.load("en_core_web_sm")
except:
    nlp_spacy = None # Fallback if not downloaded yet

class NLPModeration:
    TOXIC_KEYWORDS = ["spam", "scam", "crypto", "free money", "idiot", "stupid"]

    @staticmethod
    def analyze_message(text):
        lower_text = text.lower()
        
        # Basic Toxicity Detection (Rule-based mockup replacing scikit-learn for simplicity)
        toxicity_score = sum(0.3 for word in NLPModeration.TOXIC_KEYWORDS if word in lower_text)
        is_toxic = toxicity_score >= 0.6
        
        # NER Analysis using spaCy
        entities = []
        if nlp_spacy:
            doc = nlp_spacy(text)
            for ent in doc.ents:
                entities.append({"text": ent.text, "label": ent.label_})
                
        # Simple Spam URL detection
        url_regex = r"(https?://[^\s]+)"
        urls = re.findall(url_regex, text)
        is_spam = any("t.me/joinchat" in url for url in urls)

        return {
            "is_toxic": is_toxic,
            "toxicity_score": min(toxicity_score, 0.99),
            "is_spam": is_spam,
            "entities": entities
        }

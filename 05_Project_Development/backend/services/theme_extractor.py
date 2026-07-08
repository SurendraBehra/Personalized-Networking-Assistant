import re
import json
import logging
from typing import List, Optional
import google.generativeai as genai
from backend.app.config import settings

logger = logging.getLogger(__name__)

# List of common English stopwords for fallback extractor
STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could",
    "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for",
    "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's",
    "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm",
    "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't",
    "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours",
    "ourselves", "out", "over", "own", "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't",
    "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there",
    "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
    "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't",
    "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself",
    "yourselves", "for", "the", "and", "with", "using", "how", "what", "project", "event", "interest", "interests"
}

class ThemeExtractor:
    @staticmethod
    def extract_fallback(event_desc: str, interests: str) -> List[str]:
        """
        Extracts key phrases/keywords using basic rule-based NLP.
        """
        combined = f"{event_desc} {interests}".lower()
        # Remove punctuation
        clean_text = re.sub(r'[^\w\s-]', '', combined)
        words = clean_text.split()
        
        # Filter stopwords and short tokens
        filtered_words = [w for w in words if w not in STOPWORDS and len(w) > 3]
        
        seen = set()
        themes = []
        
        # Check for multi-word interests or event terms first
        for phrase in re.split(r'[,;.]', f"{event_desc}, {interests}"):
            phrase_clean = phrase.strip().lower()
            if phrase_clean and len(phrase_clean) > 3 and phrase_clean not in STOPWORDS:
                if len(phrase_clean.split()) <= 4:
                    phrase_formatted = phrase_clean.title()
                    if phrase_formatted not in seen:
                        seen.add(phrase_formatted)
                        themes.append(phrase_formatted)
        
        # Also add top individual keywords if list is short
        for w in filtered_words:
            w_formatted = w.title()
            if w_formatted not in seen and len(themes) < 5:
                seen.add(w_formatted)
                themes.append(w_formatted)
                
        return themes[:4]

    @classmethod
    def extract_themes(cls, event_desc: str, interests: str, api_key: Optional[str] = None) -> List[str]:
        """
        Main interface to extract key themes. Uses Gemini if API key is set, otherwise falls back.
        """
        effective_key = api_key or settings.GEMINI_API_KEY
        if not effective_key:
            logger.info("GEMINI_API_KEY not found. Running theme extraction in fallback mode.")
            return cls.extract_fallback(event_desc, interests)
        
        try:
            genai.configure(api_key=effective_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = (
                "You are an NLP model designed to extract the core professional themes or topics "
                "from a networking event description and a user's interests.\n\n"
                f"Event Description: {event_desc}\n"
                f"User Interests: {interests}\n\n"
                "Extract 2 to 4 key themes or professional topics (each theme should be 1-3 words, capitalized). "
                "Respond ONLY with a JSON array of strings. Do not include any markdown format or explanation. "
                "Example: [\"AI Ethics\", \"Sustainable Cities\", \"Urban Planning\"]"
            )
            
            response = model.generate_content(prompt)
            text = response.text.strip()
            
            if text.startswith("```"):
                text = re.sub(r"^```(?:json)?\n", "", text)
                text = re.sub(r"\n```$", "", text)
                text = text.strip()
                
            themes = json.loads(text)
            if isinstance(themes, list):
                return [str(t).title() for t in themes][:4]
            
            return cls.extract_fallback(event_desc, interests)
        except Exception as e:
            logger.error(f"Error extracting themes with Gemini API: {e}. Falling back.")
            return cls.extract_fallback(event_desc, interests)
        
ThemeExtractorInstance = ThemeExtractor()

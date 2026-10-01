"""
EcoPulse India Economic Intelligence
NLP Text Preprocessor
"""

import re
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import nltk
    from nltk.corpus import stopwords
    from nltk.tokenize import word_tokenize
    from nltk.stem import WordNetLemmatizer
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False

from helpers import setup_logging

logger = setup_logging()


class TextPreprocessor:
    """Cleans and processes economic text data."""

    def __init__(self):
        if NLTK_AVAILABLE:
            try:
                nltk.data.find('tokenizers/punkt')
            except LookupError:
                nltk.download('punkt', quiet=True)
                nltk.download('stopwords', quiet=True)
                nltk.download('wordnet', quiet=True)

            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        else:
            self.lemmatizer = None
            self.stop_words = set()

        self.nlp = None
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load('en_core_web_sm')
            except OSError:
                logger.warning("spaCy model missing. Run: python -m spacy download en_core_web_sm")

    def clean(self, text):
        """Lowercase and remove noise."""
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = re.sub(r'[^a-z\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def tokenize(self, text):
        """Tokenize cleaned text."""
        if not NLTK_AVAILABLE:
            return text.split()
        return word_tokenize(text)

    def remove_stopwords(self, tokens):
        """Filter out stopwords."""
        return [t for t in tokens if t not in self.stop_words]

    def lemmatize(self, tokens):
        """Reduce tokens to base form."""
        if self.lemmatizer is None:
            return tokens
        return [self.lemmatizer.lemmatize(t) for t in tokens]

    def extract_entities(self, text):
        """Extract named entities using spaCy."""
        if self.nlp is None:
            return []
        doc = self.nlp(text)
        return [(ent.text, ent.label_) for ent in doc.ents]

    def process(self, text):
        """Full preprocessing pipeline."""
        cleaned = self.clean(text)
        tokens = self.tokenize(cleaned)
        tokens = self.remove_stopwords(tokens)
        return self.lemmatize(tokens)


class SentimentAnalyzer:
    """Sentiment analysis for economic text."""

    def analyze(self, text):
        """Return polarity and subjectivity."""
        if not TEXTBLOB_AVAILABLE:
            return {'polarity': 0, 'subjectivity': 0, 'sentiment': 'Neutral'}

        blob = TextBlob(text)
        polarity = blob.sentiment.polarity

        if polarity > 0.1:
            sentiment = 'Positive'
        elif polarity < -0.1:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'

        return {
            'polarity': polarity,
            'subjectivity': blob.sentiment.subjectivity,
            'sentiment': sentiment
        }
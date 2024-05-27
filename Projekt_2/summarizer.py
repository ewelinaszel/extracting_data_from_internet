from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

from langdetect import detect
from googletrans import Translator

LANGUAGE = "english"
SENTENCES_COUNT = 2


def detect_language_and_translate(text):
    lang = detect(text)

    if lang != 'en':
        translator = Translator()
        try:
            translated_text = translator.translate(text, src=lang, dest='en').text
            return translated_text
        except Exception as e:
            print("Błąd podczas tłumaczenia:", e)
            return None
    else:
        return text


def summarize_text(text):
    text = detect_language_and_translate(text)
    text = text.replace(".", ". ").replace("  ", " ")

    parser = PlaintextParser.from_string(text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        sentences += str(sentence) + " "
    return sentences.strip()

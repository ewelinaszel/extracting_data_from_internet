from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
import requests

LANGUAGE = "english"
SENTENCES_COUNT = 3

def extract_text():
    # Endpoint URL for the MediaWiki API
    endpoint = "https://en.wikipedia.org/w/api.php"

    article_params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "titles": "Gemstone",  # Here come the title you want to get
        "explaintext": True  # Return plain text instead of HTML
    }
    article_response = requests.get(endpoint, params=article_params)
    if article_response.status_code == 200:
        article_data = article_response.json()
        article_text = next(iter(article_data["query"]["pages"].values()))["extract"]
        return article_text
    else:
        print("Failed to fetch article text")


def summarize_text(wiki_text):
    parser = PlaintextParser.from_string(wiki_text, Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)

    sentences = ""
    for sentence in summarizer(parser.document, SENTENCES_COUNT):
         sentences += str(sentence) + " "
    return sentences.strip()

def main():
    wiki_text = extract_text()
    with open("org.txt", "w") as text_file:
        text_file.write(wiki_text)
    wiki_text_summary = summarize_text(wiki_text)
    with open("outcome.txt", "w") as text_file:
        text_file.write(wiki_text_summary)

if __name__ == "__main__":
    main()
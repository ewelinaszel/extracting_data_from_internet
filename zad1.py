# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 22:51:49 2024

@author: Ewelina Szeliga
"""

import requests
from bs4 import BeautifulSoup
import string
import re

def get_text(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # mw-parser-output to klasa HTML uzywana na platformie MediaWiki - jest glownym kontenerem dla tresci
    content = soup.find('div', class_='mw-parser-output').text
    return content

def process_text(text):
    #Dopisz kod spelniajacy Punkt 2
    text = re.sub('[^A-Za-z0-9 ]+', '',text.lower())
    return text

def get_ranked_words(text):
    words_in_text = text.split(" ")
    ranked_words = {}
    start_value = 1
    for elem in words_in_text:
        if (elem in ranked_words.keys()):
            ranked_words[elem] = ranked_words[elem] + 1
        else:
           ranked_words[elem] = start_value  
           
    ranked_words = dict(sorted(ranked_words.items(), key = lambda w : w[1], reverse=True)[:100])

    return ranked_words

def write_results(results, filename):
    with open(filename, 'w') as file:
        number_in_ranking = 1
        for key,value in results.items():
            file.writelines(f"{number_in_ranking};{key};{value}\n")
            number_in_ranking+=1
        pass

def main():
    url = 'https://en.wikipedia.org/wiki/Web_scraping'
    text = get_text(url)
    cleaned_text = process_text(text)
    final_words = get_ranked_words(cleaned_text)
    write_results(final_words, 'output.txt')

if __name__ == "__main__":
    main()
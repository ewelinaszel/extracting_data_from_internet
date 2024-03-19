
# -*- coding: utf-8 -*-

#Celem ćwiczenia jest napisanie kodu w Pythonie, który wyszuka wszystkie linki na podanej stronie,
#a następnie w losowy sposób wybierze z nich następną stronę do odwiedzenia.
#Program powinien powtórzyć swoje działanie do momentu wyświetlenia na ekranie 100 linków.

import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin
import random
from ordered_set import OrderedSet

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)
        absolutes = [urljoin(url, link['href']) for link in links]
        return absolutes
    except requests.RequestException as e:
        print(f"Wystąpił błąd przy pobieraniu strony: {e}")
        return [] 
    
def get_not_visited_links(url,list_of_links):
    return [link for link in get_links(url) if link not in list_of_links] 
    
    
def main():
    original_url = 'https://www.agh.edu.pl/'
    list_of_links = OrderedSet()
    list_of_visited_links = []
    list_of_all_links = []
    
    current_url = original_url
    while len(list_of_links) < 100:
        print(f"Progress: {len(list_of_links)}/100")
        list_of_all_links.append(current_url)
        links = get_not_visited_links(current_url, list_of_all_links)
        if not links:
            if not list_of_visited_links:
                break
            current_url = list_of_visited_links[-1]
            list_of_visited_links = list_of_visited_links[:-1]
            continue
        list_of_links.add(current_url)
        chosen_url = random.choice(links)
        list_of_visited_links.append(current_url)
        current_url = chosen_url

    for i,link in enumerate(list_of_links):
        print(f"{i}. {link}")
    
if __name__ == "__main__":
    main()

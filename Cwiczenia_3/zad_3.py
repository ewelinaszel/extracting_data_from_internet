#Porównanie popularności tytułów pomiędzy dwoma filmowymi bazami danych
import requests
from bs4 import BeautifulSoup
import json
def get_top100(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3','Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = soup.select('.ipc-metadata-list-summary-item__c')
        top_100_list = []
        i = 0
        while len(top_100_list) < 100:
            row = sections[i]
            i += 1
            title = row.select_one('.ipc-title__text').text.split(maxsplit=1)[1]
            imdb_note = row.select_one("span[class*=pc-rating-star]").text.split(maxsplit=1)[0]
            rt_note = get_rottenTomatoes_rate(title)
            if rt_note:
                top_100_list.append({"tytul_filmu": title, "ranking_imdb": i, "ocena_imdb": imdb_note,
                                     "ocena_rotten_tomatoes": rt_note})
        return top_100_list
    except requests.RequestException as e:
        print(f"Wystąpił błąd przy pobieraniu strony: {e}")
        return []


def get_rottenTomatoes_rate(key):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9'
    }
    url = 'https://www.rottentomatoes.com/search?search='+key
    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')
    raw_info_search = soup.select("search-page-media-row")
    for elem in raw_info_search:
        title = elem.select_one('a.unset[data-qa="info-name"]').get_text(strip=True)
        note = soup.select_one('search-page-media-row[data-qa="data-row"]')['tomatometerscore']
        if title == key:
            return note
def main():
    original_url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    top100_list = get_top100(original_url)
    with open('wyniki.json', 'w') as plik:
        json.dump(top100_list, plik, indent=4)


if __name__ == "__main__":
    main()

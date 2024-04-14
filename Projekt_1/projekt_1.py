import requests
from bs4 import BeautifulSoup
import json
import re
from Projekt_1.job_info_model import JobInfoModel


def check_time(sentence):
    if re.search(r'mies\.', sentence):
        return "mies"
    elif re.search(r'godz\.', sentence):
        return "godz"
    else:
        return "brak"

def get_currency(zdanie):
    # Wyszukanie waluty (znaków "zł") w zdaniu
    waluta = re.search(r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b', zdanie)

    if waluta:
        return waluta.group(0)
    else:
        return None

def get_salary(zdanie):
    wynagrodzenie = re.findall(r'\b(\d{1,3}(?:\s?\d{3})*)–(\d{1,3}(?:\s?\d{3})*)\s', zdanie)

    if wynagrodzenie:
        min_wynagrodzenie = int(wynagrodzenie[0][0].replace('\xa0', '').replace(' ', ''))
        max_wynagrodzenie = int(wynagrodzenie[0][1].replace('\xa0', '').replace(' ', ''))
        return min_wynagrodzenie, max_wynagrodzenie

    wynagrodzenie = re.findall(r'\b(\d{1,3}(?:\s?\d{3})*)', zdanie)
    if wynagrodzenie:
        min_wynagrodzenie = int(wynagrodzenie[0].replace('\xa0', '').replace(' ', ''))
        max_wynagrodzenie = int(wynagrodzenie[0].replace('\xa0', '').replace(' ', ''))
        return min_wynagrodzenie, max_wynagrodzenie
    else:
        return None, None

def get_category(link, className):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        category = soup.select_one(className).get_text()
    except Exception as e:
        print("Cannot get category from link: {}".format(link))
        return None
    return category

def get_seniority(link, className):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        texts = [i.get_text() for i in soup.select(className)]
        possible_seniorities = ['senior', 'regular', 'mid', 'junior']
        seniorites_occurences_counts = [sum([1 for text in texts if (seniority in text.lower())]) for seniority in
                                        possible_seniorities]
        for seniority, count in zip(possible_seniorities, seniorites_occurences_counts):
            if count > 0 and seniority in ['mid', 'regular']:
                return "mid/regular"
            elif count > 0:
                return seniority
    except Exception as e:
        print("Cannot get seniority from link: {}".format(link))
        return None
    return None

def get_pracuj_offer_model(offer, num):
    link = offer.select_one('.core_n194fgoq').get('href')
    position = offer.select_one('.tiles_b1yuv00i').get_text()
    company = offer.select_one('.tiles_e1zyaun').get_text()
    salary_sentence = offer.select_one('.s1jki39v').get_text()
    currency = get_currency(salary_sentence)
    technologies = [i.get_text() for i in offer.select('.tjpooi5')]
    if check_time(salary_sentence) == "mies":
        min_salary, max_salary = get_salary(salary_sentence)
    elif check_time(salary_sentence) == "godz":
        min_salary, max_salary = get_salary(salary_sentence)
    else:
        print("Undefined time")
    category = get_category(link, '.offer-viewPFKc0t')
    seniority = get_seniority(link, '.offer-viewXo2dpV')
    return JobInfoModel(num, "pracuj.pl", link, position, company, min_salary, max_salary, currency,
                        technologies, category, seniority)

def get_technologies(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        technologies = [i.get_text() for i in soup.select('h6')]
    except Exception as e:
        print("Cannot get category from link: {}".format(link))
        return None
    return technologies

def get_just_join_offer_model(offer, num):
    link = offer.select_one('.css-4lqp8g').get('href')
    position = offer.select_one('.css-1gehlh0').get_text()
    company = offer.select_one('.css-aryx9u').get_text()
    currency = offer.select_one('.css-jmy9db').get_text()
    min_max = offer.select_one('.css-17pspck')
    span_elements = min_max.find_all('span')
    if len(span_elements) >= 2:
        min_salary = int(span_elements[0].get_text().strip().replace(' ', ''))
        max_salary = int(span_elements[1].get_text().strip().replace(' ', ''))
    technologies = get_technologies('https://justjoin.it/' + link)
    category = get_category('https://justjoin.it/' + link, '.MuiBox-root .css-6t6cyr')
    seniority = get_seniority('https://justjoin.it/' + link, '.css-15wyzmd')
    return JobInfoModel(num, "pracuj.pl", link, position, company, min_salary, max_salary, currency,
                        technologies, category, seniority)

def get_pracuj_offers(url):
    try:
        list_of_offers = []
        num = 1
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        offers = soup.select('.c1fljezf')
        for offer in offers:
            offer_model = get_pracuj_offer_model(offer, num)
            list_of_offers.append(offer_model)
            num += 1
        return list_of_offers
    except requests.RequestException as e:
        print(f"Wystąpił błąd przy pobieraniu strony: {e}")
        return []

def get_just_join_offers(just_join_url):
    try:
        list_of_offers = []
        num = 1
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(just_join_url, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        offers = soup.select('.css-1iq2gw3')
        for offer in offers:
            offer_model = get_just_join_offer_model(offer, num)
            list_of_offers.append(offer_model)
            num += 1
        return list_of_offers
    except requests.RequestException as e:
        print(f"Wystąpił błąd przy pobieraniu strony: {e}")
        return []

def main():
    just_join_url = "https://justjoin.it/krakow/data/experience-level_junior.mid.senior/remote_yes/with-salary_yes"
    pracuj_url = "https://it.pracuj.pl/praca/krakow;wp?rd=0&et=17%2C4%2C18&sal=1&its=big-data-science"
    just_join_offers = get_just_join_offers(just_join_url)
    pracuj_offers = get_pracuj_offers(pracuj_url)
    with open('pracuj_jobs.json', 'w') as plik:
        json.dump([i.__dict__ for i in pracuj_offers], plik, indent=4)
    with open('just_join_jobs.json', 'w') as plik:
        json.dump([i.__dict__ for i in just_join_offers], plik, indent=4)

if __name__ == "__main__":
    main()

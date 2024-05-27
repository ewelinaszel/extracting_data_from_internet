from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals

from data_access import connect_to_db, save_offer_in_db
from common import *

import requests
from bs4 import BeautifulSoup
import re
from Projekt_2.job_info_model import JobInfoModel


#-------------------PRACUJ PL-------------------------#
def get_currency(zdanie):
    # Wyszukanie waluty (znaków "zł") w zdaniu
    waluta = re.search(r'\b[a-zA-ZąćęłńóśźżĄĆĘŁŃÓŚŹŻ]+\b', zdanie)

    if waluta:
        return waluta.group(0)
    else:
        return None


def get_salary(zdanie, type_of_salary):
    wynagrodzenie = re.findall(r'\b(\d{1,3}(?:\s?\d{3})*)–(\d{1,3}(?:\s?\d{3})*)\s', zdanie)

    if wynagrodzenie:
        min_wynagrodzenie = int(wynagrodzenie[0][0].replace('\xa0', '').replace(' ', ''))
        max_wynagrodzenie = int(wynagrodzenie[0][1].replace('\xa0', '').replace(' ', ''))
        if type_of_salary == 2:
            return min_wynagrodzenie*168, max_wynagrodzenie*168
        return min_wynagrodzenie, max_wynagrodzenie

    wynagrodzenie = re.findall(r'\b(\d{1,3}(?:\s?\d{3})*)', zdanie)
    if wynagrodzenie:
        min_wynagrodzenie = int(wynagrodzenie[0].replace('\xa0', '').replace(' ', ''))
        max_wynagrodzenie = int(wynagrodzenie[0].replace('\xa0', '').replace(' ', ''))

        if type_of_salary == 2:
            return min_wynagrodzenie*168, max_wynagrodzenie*168
        return min_wynagrodzenie, max_wynagrodzenie
    else:
        return None, None


def check_time(sentence):
    if re.search(r'mies\.', sentence):
        return "mies"
    elif re.search(r'godz\.', sentence):
        return "godz"
    else:
        return "brak"


def get_pracuj_offer_model(offer, num):
    link = offer.select_one('.core_n194fgoq').get('href')
    position = offer.select_one('.tiles_b1yuv00i').get_text()
    company = offer.select_one('.tiles_e1zyaun').get_text()
    salary_sentence = offer.select_one('.tiles_s192qrcb').get_text()
    currency = get_currency(salary_sentence)
    technologies = [span.get_text() for span in offer.find_all('span', class_='tiles_t1eqoqxi')]
    if check_time(salary_sentence) == "mies":
        min_salary, max_salary = get_salary(salary_sentence, 1)
    elif check_time(salary_sentence) == "godz":
        min_salary, max_salary = get_salary(salary_sentence, 2)
    else:
        min_salary, max_salary = None, None
        print("Undefined time")
    category = get_category(link, '.v1xz4nnx')
    seniority = get_seniority(link, '.t1g3wgsd')
    job_description = get_job_description(link, [".tkzmjn3", ".t6laip8"])
    address = get_company_address(company)
    return JobInfoModel(num, "pracuj.pl", link, position, company, min_salary, max_salary, currency,
                        technologies, category, seniority, job_description, address)


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
        offers = soup.select('.tiles_c1k2agp8')
        for offer in offers:
            offer_model = get_pracuj_offer_model(offer, num)
            list_of_offers.append(offer_model)
            num += 1
        return list_of_offers
    except requests.RequestException as e:
        print(f"Wystąpił błąd przy pobieraniu strony: {e}")
        return []


#------------------JUST JOIN---------------------------#
def get_technologies(link):
    try:
        response = requests.get(link)
        soup = BeautifulSoup(response.text, 'html.parser')
        technologies = [i.get_text() for i in soup.select('h6')]
    except Exception:
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
    else:
        min_salary, max_salary = None, None
    technologies = get_technologies('https://justjoin.it/' + link)
    category = get_category('https://justjoin.it/' + link, '.MuiBox-root .css-6t6cyr')
    seniority = get_seniority('https://justjoin.it/' + link, '.css-15wyzmd')
    job_description = get_job_description('https://justjoin.it/' + link, [".css-6sm4q6"])
    address = get_company_address(company)
    return JobInfoModel(num, "just_join.pl", link, position, company, min_salary, max_salary, currency,
                        technologies, category, seniority, job_description, address)


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
        offers_list = soup.select('.css-1iq2gw3')
        for offer in offers_list:
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
    connection = connect_to_db()
    for offer in just_join_offers:
        save_offer_in_db(connection, offer)
    for offer in pracuj_offers:
        save_offer_in_db(connection, offer)


if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup

import summarizer as sz


def get_category(link, className):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(link, headers=header)
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


def get_job_description(link, html_class_names):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Accept-Language': 'en-US,en;q=0.9'
        }
        response = requests.get(link, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        description = ""
        for html_class in html_class_names:
            description += " ".join([el.get_text() for el in soup.select(html_class)]) + " "
        description_summary = sz.summarize_text(description)
        return description_summary
    except Exception as e:
        print("Cannot get text from link: {}".format(link))
        return None


def get_company_address(company):
    base_url = "https://nominatim.openstreetmap.org/search"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    }
    params = {
        "q": company,
        "format": "json",
        "addressdetails": 1  # Include address details in the response
    }
    response = requests.get(base_url, params=params, headers=header)
    data = response.json()

    if data:
        location = {
            "display_name": data[0]["display_name"]
        }
        return location["display_name"]
    else:
        return None

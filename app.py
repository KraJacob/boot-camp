from typing import Dict

from bs4 import BeautifulSoup
import requests
import json
import query_sample as crowler
from company.scrapping_company import Scrapping as company


class App:
    def __init__(self, web_url, nombre_article):
        self.web_url = web_url
        self.nombre_article = nombre_article

    def get_liste_article(self, startup_name):
        articles = crowler.getData(startup_name, self.nombre_article)
        return articles

    def get_liste_start_up(self):
        list_startup = company.all_start_up(self.web_url)
        return list_startup

    def get_all_startup_article(self):
        liste_startup = self.get_liste_start_up()
        list_article = []
        for startup in liste_startup:
            articles = self.get_liste_article(startup['startup_name'])
            list_article.extend(articles)

        return list_article

    def all_data(self):
        start_up_list = self.get_liste_start_up()
        startup_info_list = []

        for start_up in start_up_list:
            article = self.get_liste_article(start_up['startup_name'])
            startup_info = {
                "information_generale": start_up,
                "liste_article": article,
                "liste_publication": ""
            }
            startup_info_list.append(startup_info)

        return startup_info_list


def get_all_country_startup():
    countries = [
        {
            "url": "https://startup.info/fr/locations/afrique/cote-divoire",
            "json_file": "infos_startup_ivoirien.json"
        },
        {
            "url": "https://startup.info/fr/locations/afrique/afriquedusud/",
            "json_file": "infos_startup_souf_africa.json"
        },
        {
            "url": "https://startup.info/fr/locations/afrique/maroc/",
            "json_file": "infos_startup_maroc.json"
        },
        {
            "url": "https://startup.info/fr/locations/afrique/senegal/",
            "json_file": "infos_startup_senegal.json"
        },
        {
            "url": "https://startup.info/fr/locations/afrique/cameroun/",
            "json_file": "infos_startup_cameroun"
        }
    ]

    for country in countries:
        app = App(country['url'], 10)
        data = app.all_data()
        with open(country['json_file'], 'w') as outfile:
            json.dump(data, outfile, indent=4)


if __name__ == '__main__':
    get_all_country_startup()
    # print(test)
    # url = "https://startup.info/fr/locations/afrique/cote-divoire"
    # app = App(url, 1)
    # data = app.all_data()
    # print(data)
    # exit()
    # with open('info_startup_france.json', 'w') as outfile:
    #     json.dump(data, outfile, indent=4)

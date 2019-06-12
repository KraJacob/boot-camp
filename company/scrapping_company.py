from bs4 import BeautifulSoup
import requests
import json
from googletrans import Translator
import traceback

translator = Translator()


# next_page = True


class Scrapping:
    def __init__(self, web_url, dict_parameters):
        self.document_soup = BeautifulSoup(requests.get(web_url).text, 'html.parser')
        self.balise_companies = dict_parameters['balise_companies']
        self.tag_companies = dict_parameters['tag_companies']
        self.balise_company = dict_parameters['balise_company']
        self.tag_company = dict_parameters['tag_company']
        self.balise_company_name = dict_parameters['balise_company_name']
        self.tag_company_name = dict_parameters['tag_company_name']
        self.next_page = True
        self.web_url = web_url

    def get_next_url(self, current_url):
        try:
            soup = BeautifulSoup(requests.get(current_url).text, 'html.parser')
            lien = soup.find('nav', class_='vce-load-more').a['href']
            return lien
        except:
            lien = None
            return lien

    def get_all_url(self, current_url):
        all_url = []
        current_url = current_url
        all_url.append(current_url)
        next_page = True
        i = 0
        while next_page:
            i += 1
            try:
                next_url = self.get_next_url(current_url)
                if next_url is not None:
                    all_url.append(next_url)
                    current_url = next_url
                    # print(str(i)+ " Not None")
                else:
                    next_page = False
            except:
                print('error')
                next_page = False

        return all_url

    def get_all_company(self):
        startup = self.document_soup.find(self.balise_companies, class_=self.tag_companies)
        companies = startup.find_all(self.balise_company, class_=self.tag_company)

        data = []
        for article in companies:
            company_name = article.find(self.balise_company_name, class_=self.tag_company_name).a['href']
            company_name = company_name.split('/')
            company_name = company_name[-2]
            company = article.text
            # company_name_en = translator.translate(company_name, dest='en').text
            lien = article.find(self.balise_company_name, class_=self.tag_company_name).a['href']
            # print(translator.translate("The winter is coming !", dest='fr').text)
            try:
                posted = {
                    'startup_name': company_name.strip(),
                    'startup_name_en': company_name.strip(),
                    'startup': company.strip(),
                    'lien_satrtup_info': lien.strip()
                }
                data.append(posted)
            except:
                #     exit()
                print('une erreur est parvenue')
        return data

    def get_name(self):
        startup_name = self.document_soup.find(self.balise_company_name, class_=self.tag_company_name)
        return startup_name.text

    def all_start_up(self):
        url = "https://startup.info/fr/locations/europe-fr/france-fr/"
        with open("parameters_startup.json", 'r') as fich_param:
            param = json.loads(fich_param.read())
            scrapping = Scrapping(url, param)
            list_url = scrapping.get_all_url(url)
            data = []
            for lien in list_url:
                scrapping = Scrapping(lien, param)
                list_company = scrapping.get_all_company()
                data.extend(list_company)

        return data

if __name__ == '__main__':
    with open("parameters_startup.json", 'r') as fich_p:
        parameters = json.loads(fich_p.read())
        scraping = Scrapping('https://startup.info/fr/locations/afrique/cote-divoire',parameters)
        print(scraping.get_all_company())
        # scrapping = Scrapping(url, parameters)
        # list_post = scrapping.get_start_post_list()
        # likes = scrapping.get_start_post_like()


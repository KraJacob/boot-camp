from bs4 import BeautifulSoup
import requests
import json


class Scrapping:
    def __init__(self, web_url, dict_parameters):
        self.document_soup = BeautifulSoup(requests.get(web_url).text, 'html.parser')

        self.commentaire = dict_parameters['commentaire']
        self.commentaire_tag = dict_parameters['commentaire_tag']

        # self.comment_link = dict_parameters['comment_link']
        # self.comment_link_tag = dict_parameters['comment_link_tag']

    def get_all_comments(self):
        startup_post = self.document_soup.find_all(self.commentaire, class_=self.commentaire_tag)
        # return startup_post.find_all('div', class_='js-tweet-text-container')
        return startup_post

def get_comments(url):
    # BeautifulSoup(requests.get(url).text, 'html.parser')
    with open("publication_params.json", 'r') as fich_p:
        data = []
        try:
            parameters = json.loads(fich_p.read())
            scrapping = Scrapping(url, parameters)
            list_post = scrapping.get_all_comments()
            # print(list_post)
            posted = {}
            i = 0
            data_test = []
            for li in list_post:
                # exit()
                full_name = li.find('strong', class_="fullname show-popup-with-id u-textTruncate ").text
                comment = li.find('div', class_="js-tweet-text-container").text
                date = li.find('span', class_="_timestamp js-short-timestamp js-relative-timestamp").text
                likes = li.find('span', class_="ProfileTweet-actionCount").text
                replies = li.find('span', class_="ProfileTweet-actionCountForPresentation").text
                posted = {
                    'full_name': full_name.strip(),
                    'comment': comment.strip(),
                    'date': date.strip(),
                    'likes': likes.strip(),
                    'replies': replies.strip()
                }
                data.append(posted)
        except:
            pass

    return data


if __name__ == '__main__':
    url = "https://twitter.com/UrgentF24/status/1138046682183000065"
    texto = get_comments(url)
    print(texto)

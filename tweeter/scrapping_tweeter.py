from bs4 import BeautifulSoup
import requests
import json
import tweeter.publication_scraping as scr


class Scrapping:
    def __init__(self, web_url, dict_parameters):
        self.document_soup = BeautifulSoup(requests.get(web_url).text, 'html.parser')
        self.nom_balise = dict_parameters['nom_balise']
        self.nom_tag = dict_parameters['nom_tag']
        self.list_posts_balise = dict_parameters['list_posts_balise']
        self.list_posts_tag = dict_parameters['list_posts_tag']
        self.publication_balise = dict_parameters['publication_balise']
        self.publication_tag = dict_parameters['publication_tag']
        self.nbr_like_balise = dict_parameters['nbr_like_balise']
        self.nbr_like_tag = dict_parameters['nbr_like_tag']
        self.commentaire = dict_parameters['commentaire']
        self.commentaire_tag = dict_parameters['commentaire_tag']

        # self.comment_link = dict_parameters['comment_link']
        # self.comment_link_tag = dict_parameters['comment_link_tag']

    def getStartUpName(self):
        startup_name_document = self.document_soup.find(self.nom_balise, class_=self.nom_tag)
        return startup_name_document.string

    def get_start_post_list(self):
        startup_post = self.document_soup.find(self.list_posts_balise, id=self.list_posts_tag)
        # return startup_post.find_all('div', class_='js-tweet-text-container')
        return startup_post.find_all('div', class_='content')

    #

    def get_start_post_like(self):
        startup_post = self.document_soup.find(self.list_posts_balise, id=self.list_posts_tag)
        return startup_post.find_all('span', class_='ProfileTweet-actionCountForPresentation')

    def get_all_comments(self):
        startup_post = self.document_soup.find_all(self.commentaire, class_=self.commentaire_tag)
        # return startup_post.find_all('div', class_='js-tweet-text-container')
        return startup_post

    def get_comments(self, url):
        # BeautifulSoup(requests.get(url).text, 'html.parser')
        with open("parameters_json.json", 'r') as param:
            data = []
            try:
                parameter = json.loads(param.read())
                scrap = Scrapping(url, parameter)
                list_comment = scrap.get_all_comments()
                for comment in list_comment:
                    # exit()
                    full_name = comment.find('strong', class_="fullname show-popup-with-id u-textTruncate ").text
                    comment = comment.find('div', class_="js-tweet-text-container").text
                    comment_date = comment.find('span',
                                                class_="_timestamp js-short-timestamp js-relative-timestamp").text
                    comment_likes = comment.find('span', class_="ProfileTweet-actionCount").text
                    comment_replies = comment.find('span', class_="ProfileTweet-actionCountForPresentation").text
                    comment_data = {
                        'full_name': full_name.strip(),
                        'comment': comment.strip(),
                        'date': comment_date.strip(),
                        'likes': comment_likes.strip(),
                        'replies': comment_replies.strip()
                    }
                    data.append(comment_data)
            except:
                pass

        return data


if __name__ == '__main__':
    url = "https://twitter.com/France24_fr"

    # BeautifulSoup(requests.get(url).text, 'html.parser')
    with open("parameters_json.json", 'r') as fich_p:
        parameters = json.loads(fich_p.read())
        scrapping = Scrapping(url, parameters)
        list_post = scrapping.get_start_post_list()
        likes = scrapping.get_start_post_like()
        # print(likes)
        # exit()
        data = []
        i = 0
        for li in list_post:
            replies = li.find('div', class_="js-tweet-text-container").text
            retweet = li.find('span', class_="ProfileTweet-actionCount").text
            autor = li.find('span', class_="FullNameGroup").text
            link = 'https://twitter.com' + li.div.small.a['href']
            comments = scrapping.get_comments(link)
            print(link)
            # exit()
            try:
                date = li.find('a', class_="tweet-timestamp js-permalink js-nav js-tooltip").text
                link = 'https://twitter.com' + li.div.small.a['href']
                comments = scr.get_comments(link)
                post = li.text
                replies = li.find('div', class_="js-tweet-text-container").text
                # print("============== likes ==============")
                likes = li.find('span', class_="ProfileTweet-actionCountForPresentation").text

                posted = {
                    'post': post.strip(),
                    'likes': likes.strip(),
                    'replies': replies.strip(),
                    'retweet': retweet.strip(),
                    'autor': autor.strip(),
                    'date': date.strip(),
                    'link': link,
                    'comments': comments
                }
                data.append(posted)
            except:
                print('error')
        # jsonData = json.dump(data)
        print(data)

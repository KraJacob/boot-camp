from google import search
import pprint
import json


# KEYWORDS = 'jumia'

# data = []
# for d in search(KEYWORDS, tld='fr', lang='fr', stop=5):
# 	data.append(d)

# print (pprint.pprint(data))


class Gsearch_python:
    def __init__(self, name_search, result_number):
        self.name = name_search
        self.result_number = result_number

    def classicSearch(self):
        data = []
        for i in search(query=self.name, tld='fr', lang='fr', num=10, stop=self.result_number, pause=2):
            data.append(i)

        return data


def getData(name, limit):
    result = Gsearch_python(name, limit)
    result = result.classicSearch()

    datalist = []
    for data in result:
        datalist.append(data)

    return datalist

# result = Gsearch_python('jumia', 5)
# 	result = result.classicSearch()

# 	datalist = []
# 	for data in result:
# 	    datalist.append(data)
# with open('datalist.json', 'w') as outfile:
#     json.dump(datalist, outfile, indent=4)
# def return_article():
# pprint.pprint(getData(startup, limit))

# if __name__ == '__main__':
# google = Gsearch_python()
# print(getData('jacob',2))
# print()

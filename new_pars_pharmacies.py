import json
import requests


def get_cities(url):
    # params = {
    #     'id': '195a006a-2d78-427c-94fa-0da2aac757ba',
    #     'ipClient': '45.159.74.80',
    #     'cityGuid': 'c073f480-6d97-4af3-976b-3c069f39db52'
    # }
    
    response = requests.get(url)
    json_data = response.json()
    print(json_data)
    # return response.json()['pageProps']['cities']


# def create_cities_dict(cities):
#     city_dict = {}

#     for city in cities:
#         city_dict[city['guid']] = city['title']

#     return city_dict


# def get_cities_id(url):

#     cities = get_cities(url)
#     city_dict = create_cities_dict(cities)

#     return city_dict


if __name__ == '__main__':
    url = '    https://aptekalegko.ru/_next/data/SY0uI5MoAnmSdSWosg1JN/catalog/zabolevaniya-zheludochno-kishechnogo-trakta-i-pecheni/normalizatsiya-raboti-zhkt.json?ipClient=146.70.129.101&cityGuid=c073f480-6d97-4af3-976b-3c069f39db52&catalogLvl2=zabolevaniya-zheludochno-kishechnogo-trakta-i-pecheni&catalogLvl3=normalizatsiya-raboti-zhkt'
    get_cities(url)
    # cities_dict = get_cities_id(url)
    # print(cities_dict)

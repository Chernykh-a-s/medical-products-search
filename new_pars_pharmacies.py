import json
import requests


def get_responce_cities(url):
    response = requests.get(url)

    return response.json()['pageProps']['cities']


def create_cities_dict(cities):
    city_dict = {}

    for city in cities:
        city_dict[city['guid']] = city['title']

    return city_dict


if __name__ == '__main__':
    url = 'https://aptekalegko.ru/_next/data/SY0uI5MoAnmSdSWosg1JN/catalog/oftalmologiya/zabolevaniya-glaz.json'
   
    cities = get_responce_cities(url)

    cities_dict = create_cities_dict(cities)
   
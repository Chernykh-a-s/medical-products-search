import requests


def get_responce_cities(url):
    response = requests.get(url)

    return response.json()['pageProps']['cities']


def create_cities_dict(cities):
    city_dict = {}

    for city in cities:
        city_dict[city['guid']] = city['title']

    return city_dict

def get_responce_pharmacies(url_geo):
    result_pharmacies_cities = {}
for city in id_cities:
    url = f'https://api.garzdrav.ru:2872/Retails/{city}'
    response = requests.get(url_geo)
    result_pharmacies_cities[id_cities[city]] = response.json()
  
    json_geo = response.json()

    print(json_geo)


if __name__ == '__main__':
    url = 'https://aptekalegko.ru/_next/data/SY0uI5MoAnmSdSWosg1JN/catalog/oftalmologiya/zabolevaniya-glaz.json'
    rl_geo = 
    cities = get_responce_cities(url)

    cities_dict = create_cities_dict(cities)
   
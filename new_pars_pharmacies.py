import requests
import json


def get_responce_cities(url):
    response = requests.get(url)

    return response.json()['pageProps']['cities']


def create_cities_dict(cities):
    city_dict = {}
    for city in cities:
        city_dict[city['guid']] = city['title']

    return city_dict


def get_pharmacies_by_city(cities_dict):
    
    result_filtered = {}
    for city_id, city_name in cities_dict.items():
        url = f'https://api.garzdrav.ru:2872/Retails/{city_id}'
        response = requests.get(url)
        pharmacies = response.json()

        result_filtered[city_name] = []
        for pharmacy in pharmacies:
            result_filtered[city_name].append({
                "city": pharmacy["city"],
                "brand": pharmacy["brand"],
                "street": pharmacy["street"],
                "buildNumber": pharmacy["buildNumber"],
                "weekDayTime": pharmacy["weekDayTime"],
                "phone": pharmacy["phone"],
                "coordinates": pharmacy["coordinates"]
            })

    with open('result_filtered.json', 'w', encoding='utf-8') as f:
        json.dump(result_filtered, f, ensure_ascii=False, indent=4)

    return result_filtered


if __name__ == '__main__':
    url = 'https://aptekalegko.ru/_next/data/SY0uI5MoAnmSdSWosg1JN/catalog/oftalmologiya/zabolevaniya-glaz.json'
   
    cities = get_responce_cities(url)

    cities_dict = create_cities_dict(cities)

    result_pharmacies_cities = get_pharmacies_by_city(cities_dict)

    
   
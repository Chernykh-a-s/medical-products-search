import json


with open('id_cities_before_processing.json', 'r', encoding='utf-8') as file:
    data = json.load(file)


cities = data['pageProps']['cities']


city_dict = {}

for city in cities:
    city_dict[city['guid']] = city['title']


print(city_dict)


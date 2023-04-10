import requests
import json

with open('id_cities.json', 'r', encoding='utf-8') as file:
    id_cities = json.load(file)

result_pharmacies_cities = {}
for city in id_cities:
    url = f'https://api.garzdrav.ru:2872/Retails/{city}'
    response = requests.get(url)
    result_pharmacies_cities[id_cities[city]] = response.json()

with open('result.json', 'w', encoding='utf-8') as file:
    json.dump(result_pharmacies_cities, file, ensure_ascii=False, indent=4)
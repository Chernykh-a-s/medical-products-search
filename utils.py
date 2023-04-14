from geopy.distance import geodesic
import json
from telegram import ReplyKeyboardMarkup, KeyboardButton


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


DRUGS = [
    {
        'name': 'Аквалор беби',
        'brand': 'АКВАЛОР',
        'variants': [
            {'option': '150 мл мягкий душ', 'price': 449.00},
            {'option': '15 мл капли', 'price': 237.00},
        ]
    },
    {
        'name': 'Комбилипен',
        'brand': 'Фармстандарт-Уфимский витаминный завод,ОАО',
        'variants': [
            {'option': 'раствор для внутримышечного введения 2 мл ампулы 5 шт.', 'price': 234.00},
            # {'option': 'раствор для внутримышечного введения 2 мл ампулы 10 шт.', 'price': 330.00},
        ]
    }
]


def get_user_input(update, context):
    search_query = update.message.text.lower().strip()
    
    return search_query


def search_drug(search_query):
    matches_drugs = []
    
    for drug in DRUGS:
        if search_query in drug['name'].lower():
            matches_drugs.append(drug)
            
    return matches_drugs


def send_drug_info(update, matches_drugs):
    if not matches_drugs:
        update.message.reply_text(f"К сожалению, я не нашел лекарств по вашему запросу.", reply_markup = main_keyboard())

    for drug in matches_drugs:
        update.message.reply_text(build_message(drug), reply_markup = main_keyboard())


def build_message(drug):
    message = f"Название: {drug['name']}\nПроизводитель: {drug['brand']}\nВарианты:\n"

    if len(drug['variants']) == 1:
        message += format_variant(drug['variants'][0])
    else:
        message += build_variant_list(drug['variants'])

    message += "\n"

    return message


def build_variant_list(variants):
    variants_list = ""

    for item, variant in enumerate(variants, start=1):
        variants_list += format_variant(variant, item) + "\n"

    return variants_list


def format_variant(variant, item_number=None):
    if item_number is None:
        return f"{variant['option']} - {variant['price']} руб."
    
    return f"{item_number}. {variant['option']} - {variant['price']} руб."


def main_keyboard():
    return ReplyKeyboardMarkup([[KeyboardButton('Ближайшие аптеки', request_location=True), 'Справка' ]], resize_keyboard=True)


def load_pharmacies_data():
    with open('pharmacies.json', 'r') as f:
        pharmacies_data = json.load(f)

    return pharmacies_data


def get_distance(user_lat, user_lon, pharmacy_lat, pharmacy_lon):
    user_coord = (user_lat, user_lon)
    pharmacy_coord = (pharmacy_lat, pharmacy_lon)

    return geodesic(user_coord, pharmacy_coord).km


def get_pharmacy_info(pharmacy):
    info = f'Название: {pharmacy["brand"]}\nАдрес: {pharmacy["street"]} {pharmacy["buildNumber"]}\nВремя работы: {pharmacy["weekDayTime"]}\nТелефон: {pharmacy["phone"]}\n\n'
  
    return info


def get_nearest_pharmacies(user_lat, user_lon, n=3):
    pharmacies_data = load_pharmacies_data()

    distances = {}  
    for city, pharmacies_list in pharmacies_data.items():
        for pharmacy in pharmacies_list:
            pharmacy_lat, pharmacy_lon = pharmacy['coordinates']
            distance = get_distance(user_lat, user_lon, pharmacy_lat, pharmacy_lon)
            distances[(city, pharmacy['brand'])] = {'distance': distance, 'pharmacy': pharmacy}

    nearest_pharmacies = sorted(distances.items(), key=lambda x: x[1]['distance'])[:n]

    message = 'Ближайшие аптеки:\n\n'
    for i, ((city, brand), data) in enumerate(nearest_pharmacies, 1):
        distance = data['distance']
        pharmacy_info = get_pharmacy_info(data['pharmacy'])
        message += f'{i}. {brand} в г. {city} ({distance:.2f} км)\n'
        message += pharmacy_info

    return message

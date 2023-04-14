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
    return ReplyKeyboardMarkup([['Ближайшие аптеки', KeyboardButton('Мои координаты', request_location=True) ]], resize_keyboard=True)
    

def open_pharmacies_data():
    with open("pharmacies.json", "r", encoding="utf-8") as data:
        pharmacies_data = json.load(data)
    return pharmacies_data

def get_pharmacy_distance(pharmacy, user_location):
    return geodesic(user_location, pharmacy["coordinates"]).km

def get_pharmacy_info(pharmacy):
    info = f"Город: {pharmacy['city']}\n"
    info += f"Название: {pharmacy['brand']}\n"
    info += f"Адрес: {pharmacy['street']}, {pharmacy['buildNumber']}\n"
    info += f"Время работы: {pharmacy['weekDayTime']}\n"
    info += f"Телефон: {pharmacy['phone']}\n"
    info += f"Расстояние: {pharmacy['distance']:.2f} км\n"
    return info

def get_nearest_pharmacies(pharmacies_data, user_location, n=5):
    distances = []
    for city, pharmacies in pharmacies_data.items():
        for pharmacy in pharmacies:
            distance = get_pharmacy_distance(pharmacy, user_location)
            distances.append({"pharmacy": pharmacy, "distance": distance})
    sorted_pharmacies = sorted(distances, key=lambda p: p["distance"])[:n]
    return sorted_pharmacies


    
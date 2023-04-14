from geopy.distance import geodesic
import json
from telegram import ReplyKeyboardMarkup, KeyboardButton


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def load_drugs_data():
    with open('drugs.json', 'r') as file:
        drugs_data = json.load(file)

    return drugs_data


def get_user_input(update, context):
    search_query = update.message.text.lower().strip()
    
    return search_query


def search_drug(search_query):
    matches_drugs = []
    
    for drug in load_drugs_data():
        if search_query in drug['product_name'].lower():
            matches_drugs.append(drug)
            
    return matches_drugs


def send_drug_info(update, matches_drugs):
    if not matches_drugs:
        update.message.reply_text(f"К сожалению, я не нашел медикаментов по вашему запросу.", reply_markup = main_keyboard())

    for index, drug in enumerate(matches_drugs, start=0):
        update.message.reply_text(build_message(drug, index), reply_markup = main_keyboard())


def build_message(drug, index):
    message = f"{index + 1}. Название: {drug['product_name']}\n\nПроизводитель: {drug['manufacturer']}\n\nЦена: {drug['price']} руб."

    return message


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

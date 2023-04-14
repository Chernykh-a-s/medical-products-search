from utils import get_user_input, search_drug, send_drug_info, main_keyboard, open_pharmacies_data, get_nearest_pharmacies, get_pharmacy_info

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def great_user(update, context):
    update.message.reply_text(f'Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужные медикаменты в аптеках рядом с вами.🚑')
    update.message.reply_text(f'Для поиска медикаментов - введите название', reply_markup = main_keyboard())
    
    logger.info('Вызван /start') 


def medicines(update, context):
    user_input = get_user_input(update, context)
    matches = search_drug(user_input)
    send_drug_info(update, matches)


def user_coordinates(update, context):
    user_coord = update.message.location
    update.message.reply_text(f'Ваши координаты {user_coord}', reply_markup = main_keyboard())
    return user_coord

def search_pharmacies(update, context):
    user_location = (update.message.location)
    pharmacies_data = open_pharmacies_data()
    nearest_pharmacies = get_nearest_pharmacies(pharmacies_data, user_location)
    message = "Ближайшие аптеки:\n"
    for pharmacy_data in nearest_pharmacies:
        pharmacy = pharmacy_data["pharmacy"]
        distance = pharmacy_data["distance"]
        pharmacy["distance"] = distance
        message += get_pharmacy_info(pharmacy) + "\n"
    logger.info('Найдены аптеки') 
from utils import get_user_input, search_drug, send_drug_info, main_keyboard, get_nearest_pharmacies


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def great_user(update, context):
    update.message.reply_text(f'Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужные медикаменты в аптеках рядом с вами.🚑')
        
    logger.info('Вызван /start') 


def medicines(update, context):
    user_input = get_user_input(update, context)
    matches = search_drug(user_input)
    send_drug_info(update, matches)


def user_coordinates(update, context):
    user_lat = update.message.location.latitude
    user_lon = update.message.location.longitude
    message = get_nearest_pharmacies(user_lat, user_lon)
    update.message.reply_text(message, reply_markup = main_keyboard())

def help(update, context):
    update.message.reply_text(f'Для поиска медикаментов - введите название.\n\nДля поиска ближайших аптек - нажмите кнопку "Ближайшие аптеки" или поделитесь Геопозицией', reply_markup = main_keyboard())  
    
from telegram import ReplyKeyboardMarkup


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


drugs = [
    {
        'name': 'Аквалор беби',
        'brand': 'АКВАЛОР',
        'variants': [
            {'option': '150 мл мягкий душ', 'price': 449.00},
            {'option': '15 мл капли', 'price': 237.00}
        ]
    },
    {
        'name': 'Комбилипен',
        'brand': 'Фармстандарт-Уфимский витаминный завод,ОАО',
        'variants': [
            {'option': 'раствор для внутримышечного введения 2 мл ампулы 5 шт.', 'price': 234.00},
            {'option': 'раствор для внутримышечного введения 2 мл ампулы 10 шт.', 'price': 330.00}
        ]
    }
]


def great_user(update, context):
    # start_keyboard = ReplyKeyboardMarkup([['Поиск лекарства']], resize_keyboard=True)

    update.message.reply_text('Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужное лекарство в аптеках рядом с вами.🚑')
    update.message.reply_text('Для поиска лекарства - введите название лекарства  ')
    
    logger.info('Вызван /start') 


def text_handler(update, context):
    user_input = get_user_input(update, context)
    matches = search_medicine(user_input)
    send_medicine_info(update, matches)


def get_user_input(update, context):
    user_input = update.message.text.lower().strip()
    return user_input


def search_medicine(user_input):
    matches = []
    
    for medicine in drugs:
        if user_input in medicine['name'].lower():
            matches.append(medicine)
            
    return matches


def send_medicine_info(update, matches):
    if not matches:
        update.message.reply_text("К сожалению, я не нашел лекарств по вашему запросу.")
        return
    
    message = ""
    
    for match in matches:
        message += f"Название: {match['name']}\n"
        message += f"Производитель: {match['brand']}\n"
        message += "Варианты:\n"
        
        if len(match['variants']) == 1:
            message += f"{match['variants'][0]['option']} - {match['variants'][0]['price']} руб.\n"
        else:
            for i, variant in enumerate(match['variants'], start=1):
                message += f"{i}. {variant['option']} - {variant['price']} руб.\n"
        
        message += "\n"
    
    update.message.reply_text(message)


# 2) сделать нумерацию найденых лекарств , если их больше одного найдено
# 3) Добавить кнопку для поиска лекарств
# 4) сделать привязку парсера к гео
# 5) Выводить ближайшие аптеки, где можно забрать лекарства
# 6)Сделать поиск лекарства кнопочкой
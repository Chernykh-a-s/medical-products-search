from telegram import ReplyKeyboardMarkup


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def great_user(update, context):
    start_keyboard = ReplyKeyboardMarkup([['Поиск лекарства']], resize_keyboard=True)

    update.message.reply_text('Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужное лекарство в аптеках рядом с вами.🚑')
    update.message.reply_text('Для поиска лекарства - нажмите на кнопку внизу экрана  ', reply_markup=start_keyboard)
    
    logger.info('Вызван /start') 


def find_drug_button(update, context):
    user_drug_find = update.message.text
    
    if user_drug_find == 'Поиск лекарства':
        update.message.reply_text('Введите название лекарства')
    else:
        update.message.reply_text(f'Выбрано лекарство: {user_drug_find}')
        
        logger.info(user_drug_find)

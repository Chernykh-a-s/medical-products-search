from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import settings

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def great_user(update, context):
    start_keyboard = ReplyKeyboardMarkup([['Поиск лекарства']],resize_keyboard=True)
    update.message.reply_text('Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужное лекарство в аптеках рядом с вами.🚑')
    update.message.reply_text('Для поиска лекарства - наберите команду drug/ и через пробел название лекарства. Или нажмите на кнопку внизу экрана', reply_markup=start_keyboard)
    logger.info('Вызван /start') 

def find_drug(update, context):
    user_drug = context.args[0]
    update.message.reply_text(f'Выбрано лекарство: {user_drug}')
    logger.info(user_drug) 

def find_drug_button(update, context):
    update.message.reply_text('Введите лекарство')

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',great_user))
    dp.add_handler(CommandHandler('drug', find_drug))
    dp.add_handler(MessageHandler(Filters.regex('^(Поиск лекарства)$'),find_drug_button))

    logger.info('Бот запущен') 
    
    mybot.start_polling()
    mybot.idle()

if __name__ == '__main__':
    main()
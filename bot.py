import logging
import settings
from telegram.ext import Updater, CommandHandler

logging.basicConfig(filename='bot.log', level=logging.INFO)
logger = logging.getLogger(__name__)

def great_user(update, context):
    logger.info('Вызван /start')
    # Доделать нормальное приветствие
    update.message.reply_text('Привет пользователь, данный бот умеет искать лекарста.') 

def main():
    mybot = Updater(settings.API_KEY, use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',great_user))
    logger.info('Бот запущен') 
    mybot.start_polling()
    mybot.idle()

main()

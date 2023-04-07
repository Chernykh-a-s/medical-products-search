from handlers import great_user, text_handler
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


import settings


import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    mybot = Updater(settings.API_KEY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start',great_user))
    dp.add_handler(MessageHandler(Filters.text, text_handler))
    
    
  
    mybot.start_polling()
    mybot.idle()

    logger.info('Бот запущен') 


if __name__ == '__main__':
    main()
    
from utils import get_user_input, search_drug, send_drug_info

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def great_user(update, context):
  
    update.message.reply_text('Привет! Я чат бот СправАптека. Работаю 2️⃣4️⃣ / 7️⃣, без выходных и перерывов. Помогу Вам найти нужное лекарство в аптеках рядом с вами.🚑')
    update.message.reply_text('Для поиска лекарства - введите название лекарства  ')
    
    logger.info('Вызван /start') 


def text_handler(update, context):
    user_input = get_user_input(update, context)
    matches = search_drug(user_input)
    send_drug_info(update, matches)

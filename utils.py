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
def get_user_input(update, context):
    user_drug = update.message.text.lower().strip()
    
    return user_drug


def search_drug(user_drug):
    matches_drugs = []
    
    for drug in drugs:
        if user_drug in drug['name'].lower():
            matches_drugs.append(drug)
            
    return matches_drugs


def send_drug_info(update, matches_drugs):
    if not matches_drugs:
        update.message.reply_text("К сожалению, я не нашел лекарств по вашему запросу.")
        return
    
    message = ""
    
    for drug in matches_drugs:
        message += f"Название: {drug['name']}\n"
        message += f"Производитель: {drug['brand']}\n"
        message += "Варианты:\n"
        
        if len(drug['variants']) == 1:
            message += f"{drug['variants'][0]['option']} - {drug['variants'][0]['price']} руб.\n"
        else:
            for i, variant in enumerate(drug['variants'], start=1):
                message += f"{i}. {variant['option']} - {variant['price']} руб.\n"
        
        message += "\n"
    
    update.message.reply_text(message)
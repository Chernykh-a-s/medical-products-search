import requests

print('Введите api категории')
category = input()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}

response = requests.get(category, headers=headers)

medicine_list = response.json()["result"]
sum_of_page_medicine_list = response.json()["totalCount"] // response.json()["currentCount"]

for page in range(sum_of_page_medicine_list+1):
    if page == 0:
        for medicine in medicine_list:
            title = medicine["tradeName"]
            price = medicine["minPrice"]
            last_price = medicine["lastMinPrice"]
            if price == 0:
                url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
                print(f"Препарата {title} нет в наличии. Последняя цена: {last_price} {url=}")
            else:
                url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
                print(f"Препарат: {title} цена: {price} url: {url=}")
    else:
        category = category.replace(f'page={page-1}', f'page={page}')
        response = requests.get(category, headers=headers)
        medicine_list = response.json()["result"]
        sum_of_page_medicine_list = response.json()["totalCount"] // response.json()["currentCount"]
        for medicine in medicine_list:
            title = medicine["tradeName"]
            price = medicine["minPrice"]
            last_price = medicine["lastMinPrice"]
            if price == 0:
                url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
                print(f"Препарата {title} нет в наличии. Последняя цена: {last_price} {url=}")
            else:
                url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
                print(f"Препарат: {title} цена: {price} url: {url=}")

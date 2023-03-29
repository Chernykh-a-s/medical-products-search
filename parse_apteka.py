import requests


def getting_category_from_the_user():
    print('Введите api категории')
    category = input()
    return category


def receive_data_from_the_pharmacy(category):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
}

    response = requests.get(category, headers=headers)

    medicine_list = response.json()["result"]
    sum_of_page_medicine_list = response.json()["totalCount"] // response.json()["currentCount"]
    return medicine_list, sum_of_page_medicine_list


def loop_to_output_data_from_pharmacy(medicine_list):
    for medicine in medicine_list:
        title = medicine["tradeName"]
        price = medicine["minPrice"]
        last_price = medicine["lastMinPrice"]
        if price == 0:
            url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
            print(f"Препарата {title} нет в наличии. Последняя цена: {last_price} р., url: {url}")
        else:
            url = f"https://apteka.ru/product/{medicine['humanableUrl']}"
            print(f"Препарат: {title}, Цена: {price} р., url: {url}")


def data_output_from_the_pharmacy(medicine_list, sum_of_page_medicine_list, category):
    for page in range(sum_of_page_medicine_list):
        params = {'page': page}
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        }
        while True:
            response = requests.get(category, params=params, headers=headers)
            medicine_list = response.json()["result"]
            sum_of_page_medicine_list = response.json()["totalCount"] // response.json()["currentCount"]
            loop_to_output_data_from_pharmacy(medicine_list)
            if not response.links.get('next'):
                break

            params = {'page': int(params['page']) + 1}


if __name__ == "__main__":
    category = getting_category_from_the_user()
    medicine_list, sum_of_page_medicine_list = receive_data_from_the_pharmacy(category)
    loop_to_output_data_from_pharmacy(medicine_list)
    data_output_from_the_pharmacy(medicine_list, sum_of_page_medicine_list, category)
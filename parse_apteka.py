import requests


def getting_category_from_the_user():
    category_api_link = input('Введите api категории')
    return category_api_link


def receive_data_from_the_pharmacy(category_api_link):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    }

    response = requests.get(category_api_link, headers=headers)
    sum_of_page_medicine_list = response.json()["totalCount"] // response.json()["currentCount"]
    params = {}
    for page in range(sum_of_page_medicine_list + 1):
        params[page] = page

    response_with_params = requests.get(category_api_link, headers=headers, params=params)

    return response_with_params


def processing_data_from_the_pharmacy(response_with_params):
    medicine_list = response_with_params.json()["result"]
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
    return medicine_list


def data_output_from_the_pharmacy(category_api_link, response_with_params):
    receive_data_from_the_pharmacy(category_api_link)
    processing_data_from_the_pharmacy(response_with_params)


if __name__ == "__main__":
    category_api_link = getting_category_from_the_user()
    response_with_params = receive_data_from_the_pharmacy(category_api_link)
    medicine_list = processing_data_from_the_pharmacy(response_with_params)
    data_output_from_the_pharmacy(category_api_link, response_with_params)

import requests
import json
import time
import configparser


def get_proxy_from_settings():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return {'http': config["Proxy"]["proxy"], 'https': config["Proxy"]["proxy"]}


def get_ip_from_settings():
    config = configparser.ConfigParser()
    config.read("settings.ini")
    return config["Proxy"]["ip"]


def make_request_with_proxy(url, params):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    }
    proxies = get_proxy_from_settings()
    response = requests.get(url=url, headers=headers, proxies=proxies, params=params)
    return response


def load_json_with_pharmacy_categories():
    with open('category_aptekaleg.json', 'r', encoding='utf-8') as f:
        return json.load(f)


def receive_category_from_json(json_file):
    pharmacy_categories = []
    for name_of_category, category_for_parse in json_file_with_apteka_categories.items():
        for name_of_category in category_for_parse:
            category_subcategory_for_url = str(name_of_category['category']) + '/' + str(name_of_category[
                                                                                             'subcategory'])
            pharmacy_categories.append(category_subcategory_for_url)
    return pharmacy_categories


def parse_apteka(pharmacy_categories, json_file_with_apteka_categories):

    ip = get_ip_from_settings()

    url = 'https://aptekalegko.ru/_next/data/SY0uI5MoAnmSdSWosg1JN/catalog/{}.json'
    params = {
        'pages': None,
        'order': 'None',
        'ipClient': ip,
        'cityGuid': 'c073f480-6d97-4af3-976b-3c069f39db52',
        'catalogLvl2': None,
        'catalogLvl3': None
    }

    for page in range(1):
        params['pages'] = page + 1

    urls_category = []
    for category in pharmacy_categories:
        url_format = url.replace('{}', category)
        urls_category.append(url_format)
        print(urls_category)

    for category in urls_category:
        response = make_request_with_proxy(category, params=params)
        try:
            count_of_pages = response.json()["pageProps"]["products"]["count"] // len(response.json()["pageProps"][
                                                                                          "products"]["products"]) + 1
        except ZeroDivisionError:
            continue

        for page in range(count_of_pages):
            params['pages'] = page + 1
            response = make_request_with_proxy(category, params=params)
            medicine_list = response.json()["pageProps"]["products"]["products"]

            for product in medicine_list:
                one_position_of_product = {}
                product_name = product["product"]
                manufacturer = product["manufacturer"]
                price = product["price"]
                one_position_of_product = {
                    'product_name': product_name,
                    'manufacturer': manufacturer,
                    'price': price,
                }

                with open("drugs.json", "a", encoding='utf-8') as f:
                    json.dump(one_position_of_product, f, indent=4, ensure_ascii=False)
                    f.write(','), f.write('\n')


if __name__ == '__main__':
    json_file_with_apteka_categories = load_json_with_pharmacy_categories()
    receive_category_from_json(json_file_with_apteka_categories)
    pharmacy_categories = receive_category_from_json(json_file_with_apteka_categories)
    parse_apteka(pharmacy_categories, json_file_with_apteka_categories)

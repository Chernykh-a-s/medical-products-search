import requests
from bs4 import BeautifulSoup
import json
import time


def get_proxies():
    with open('proxy.txt', 'r') as f:
        proxies = {'http': f.readline().strip(), 'https': f.readline().strip()}
    return proxies

def get_ip():
    with open('ip.txt', 'r') as f:
        ip = f.readline().strip()
    return ip

def make_request(url):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
    }
    proxies = get_proxies()
    response = requests.get(url=url, headers=headers, proxies=proxies)
    return response


def receive_category_links(response):

    soup = BeautifulSoup(response.text, 'html.parser')

    list_data_pharmacy = soup.find('ul', '_sectionBadLekarstva_ul__DQ4zv').find_all('a')

    category_links = {}

    for link in list_data_pharmacy:
        url = link.get("href")
        text = link.text
        category_links[text] = f'https://aptekalegko.ru/{url}'

    return category_links

def receive_subcategory_links(response):

    soup = BeautifulSoup(response.text, 'html.parser')

    list_data_pharmacy = soup.find('ul', '_catalogLvl2_ul__xJ8Jo').find_all('a')

    subcategory_links = {}

    for link in list_data_pharmacy:
        url = link.get("href")
        text = link.text
        subcategory_links[text] = f'https://aptekalegko.ru/{url}'

    return subcategory_links

def write_category_links_in_json(file_name, category_links):

    with open(file_name, 'a', encoding='utf-8') as file:
        json.dump(category_links, file, indent=4, ensure_ascii=False)


def write_subcategory_links_in_json():
    with open('category_links.json', encoding="utf-8") as fh:
        data = json.loads(fh.read())

    file_name = 'subcategory_links.json'

    for category_name, url in data.items():
        response = make_request(url)
        subcategory_links = receive_subcategory_links(response)
        write_category_links_in_json(file_name,  subcategory_links)
        time.sleep(7)


def parse_api():
    data_for_parse = {
        'category': 'oftalmologiya',
        'subcategory': 'zabolevaniya-glaz',
    }

    sum_of_pages = 13
    ip = get_ip()

    address_template_api = 'https://aptekalegko.ru/_next/data/FUDDCaS8piyfZMougusFc/catalog/{}' \
                           '/{}.json?pages=&order=None&ipClient={}&cityGuid=c073f480-6d97' \
                           '-4af3-976b-3c069f39db52&catalogLvl2={}&catalogLvl3={}'.format(
        data_for_parse['category'], data_for_parse['subcategory'], ip, data_for_parse['category'], data_for_parse[
            'subcategory'])

    links_api_for_parse = {}

    for page in range(sum_of_pages):
        link = address_template_api.replace('pages=', 'pages='+str(page+1))
        links_api_for_parse[f'page: {page+1}'] = link

    drugs = []
    one_position_of_product = {}

    for page, link in links_api_for_parse.items():
        response = make_request(link)
        medicine_list = response.json()["pageProps"]["products"]["products"]
        time.sleep(5)
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
            drugs.append(one_position_of_product)

    with open("drugs.json", "a", encoding='utf-8') as f:
        json.dump(drugs, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    get_links_from_jsons_for_parse_api()

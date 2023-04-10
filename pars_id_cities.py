import json
import requests


cookies = {
    '_ym_uid': '1681151585680010903',
    '_ym_d': '1681151585',
    '_ym_isad': '2',
    '_ym_visorc': 'w',
    'c_guid': 'c073f480-6d97-4af3-976b-3c069f39db52',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    # 'Cookie': '_ym_uid=1681151585680010903; _ym_d=1681151585; _ym_isad=2; _ym_visorc=w; c_guid=c073f480-6d97-4af3-976b-3c069f39db52',
    'Referer': 'https://www.google.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


response = requests.get('https://aptekalegko.ru/_next/data/FUDDCaS8piyfZMougusFc/compilations.json?id=195a006a-2d78-427c-94fa-0da2aac757ba&ipClient=45.159.74.80&cityGuid=c073f480-6d97-4af3-976b-3c069f39db52', cookies=cookies, headers=headers)


cities = response.json()['pageProps']['cities']

city_dict = {}

for city in cities:
    city_dict[city['guid']] = city['title']
  
with open('id_cities.json', 'w', encoding='utf-8') as file:
    json.dump(city_dict, file, indent=4, ensure_ascii=False ) 

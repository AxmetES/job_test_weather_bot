import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin
import pprint


def get_soup(main_url):
    response = requests.get(main_url, headers={'User-Agent': UserAgent().chrome})
    soup = BeautifulSoup(response.text, 'lxml')
    return soup


def get_split(weather):
    split = weather.split()
    morning = ''.join(split[:2])
    day_timem = ''.join(split[2:4])
    evening = ''.join(split[4:6])
    night = ''.join(split[6:8])
    wind = ''.join(split[8:13])
    humidity_base = ''.join(split[11:13])
    pressure = ''.join(split[13:])
    return morning, day_timem, evening, night, wind, pressure


def get_weather():
    main_url = 'https://goodmeteo.ru/pogoda-yaroslavl/mesyac/'
    base_url = 'https://goodmeteo.ru/pogoda-yaroslavl/'
    storage = []

    month = get_soup(main_url).select('.m_bl')[0]
    for day in month:
        date = day.select_one('a').text.strip()
        url = urljoin(base_url, day.select_one('a')['href'])
        day_weather = get_soup(url).select('.det_pog_b2_sm')
        for day_info in day_weather:
            weather = day_info.text
            morning, day_time, evening, night, wind, pressure = get_split(weather)
            storage.append({
                'date': date,
                'morning': morning,
                'day_time': day_time,
                'evening': evening,
                'night': night,
                'wind': wind,
                'pressure': pressure,
            })

    return storage


if __name__ == '__main__':
    storage = get_weather()

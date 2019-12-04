from datetime import datetime
from multiprocessing.pool import ThreadPool

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

months = {'Jan': '1', 'Feb': '2', 'Mar': '3', 'Apr': '4', 'May': '5', 'Jun': '6',
          'Jul': '7', 'Aug': '8', 'Sep': '9', 'Oct': '10', 'Nov': '11', 'Dec': '12'}
site_url = 'https://www.lueftner-cruises.com'
cruises_url = 'https://www.lueftner-cruises.com/en/river-cruises/cruise.html'


def get_cruises_links():
    response = requests.get(cruises_url, headers={'User-Agent': UserAgent().chrome})
    if response.status_code != 200:
        raise ConnectionError(f'{cruises_url} request status_code is {response.status_code} != 200')

    html = response.content
    soup = BeautifulSoup(html, 'html.parser')

    cruises_soups = soup.select('h3.travel-box-heading > span > a')

    cruises_links = [site_url + a['href'] for a in cruises_soups]
    return cruises_links


def fetch_cruise(url):
    response = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    if response.status_code != 200:
        raise ConnectionError(f'{url} not downloaded correctly: {response.status_code}')
    return response.content


def parse_date_ship_price(elem):
    start_end_str = elem.find('span', class_='price-duration').text
    start_end = []
    for string in start_end_str.split(' - '):
        for month in months:
            if month in string:
                string = string.replace(month, months[month])
                break
        start_end.append(datetime.strptime(string, '%d. %m %Y'))

    start, end = start_end

    ship = elem.find('span', class_='table-ship-name').text
    price = elem.find('span', class_='big-table-font').text
    price = price.strip().split(' ')[1]
    price = float(price.replace(',', '').replace('.', '')) / 100

    date = start.strftime('%Y-%m-%d')
    return date, ship, price


def parse_cruise(url):
    html = fetch_cruise(url)
    soup = BeautifulSoup(html, 'html.parser')
    name = soup.select('div.cruise-headline > h1')[0].text
    duration = soup.find('p', class_='cruise-duration').text
    duration = int(duration.strip().split(' ')[0])
    itinerary = soup.find_all('span', class_='route-city')
    itinerary = [city.text.replace('\n', '').strip() for city in itinerary]
    itinerary = [
        city.strip()
        for cities in itinerary
        for city in cities.split('>')
    ]
    dates_elems = soup.select('div.main-cabin-heading > a')
    dates = [{
        date: {
            'ship': ship,
            'price': price
        } for date, ship, price in [parse_date_ship_price(elem) for elem in dates_elems]
    }]

    cruise = {
        'name': name,
        'days': duration,
        'itinerary': itinerary,
        'dates': dates,
    }
    return cruise


def parse_all_cruises(urls):
    pool = ThreadPool(10)
    results = pool.imap_unordered(parse_cruise, urls)
    pool.close()
    pool.join()
    return results


def get_cruises(amount=4):
    cruises_links = get_cruises_links()[:amount]
    cruises = list(parse_all_cruises(cruises_links))
    return cruises

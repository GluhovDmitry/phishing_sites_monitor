import requests
import json

from loguru import logger
from bs4 import BeautifulSoup

from mainApp import models

def parse_html(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html5lib')

        table = soup.findChildren('table')
        my_table = table[0]

        rows = my_table.findChildren(['tr'])
        for row in rows:
            cells = row.findChildren('td')
            if cells:
                sites = [cell.strip() for cell in cells[3].text.strip().split('\n')]
                data_loader(number=int(cells[1].text), title=cells[2].text, urls=sites)

    except Exception as e:
        logger.error(str(e))
    else:
        logger.info('loading success')

def data_loader(number, title, urls):
    models.Banks.objects.create(number=number, title=title, urls=urls)


if __name__ == '__main__':
    parse_html('https://cbr.ru/banking_sector/credit/cowebsites/')
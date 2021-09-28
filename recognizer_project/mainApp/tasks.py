from celery import shared_task
from loguru import logger

from mainApp.celery import app
from services import banks_data_parser

@app.task
def parser_task():
    banks_data_parser.parse_html('https://cbr.ru/banking_sector/credit/cowebsites/')

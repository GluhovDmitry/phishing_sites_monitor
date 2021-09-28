from django.shortcuts import render
from mainApp.services import banks_data_parser

def parser():
    banks_data_parser.parse_html('https://cbr.ru/banking_sector/credit/cowebsites/')

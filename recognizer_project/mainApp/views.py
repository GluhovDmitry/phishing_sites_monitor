from django.shortcuts import render
from mainApp.services import banks_data_parser
from django.shortcuts import render, get_object_or_404
from .models import Banks, FakeUrls
from loguru import logger

def parser():
    banks_data_parser.parse_html('https://cbr.ru/banking_sector/credit/cowebsites/')


def home(request):
    return render(request, 'home.html', {})


def banks(request):
    banks = Banks.objects.all()
    return render(request, 'banks.html', {'banks': banks})


def bank_detail(request, pk):
    bank = get_object_or_404(Banks, pk=pk)
    fakes = FakeUrls.objects.filter(title=bank)
    return render(request, 'bank_detail.html', {'bank': bank, 'fakes': fakes})


def recognizer(request):
    return render(request, 'recognizer.html', {})
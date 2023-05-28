import datetime
import threading
import time

import pandas as pd
import yfinance as yf
from mysite.average import  *
from django.shortcuts import render
import requests, json
from django.http import HttpResponse
from mysite.models import *
# Create your views here.
def stockAnalysis(request):
    stocks = Stock_name.objects.all()
    return render(request, 'stockAnalysis.html', locals())

def backtesting(request):
    stocks = Stock_name.objects.all()
    return render(request, 'backtesting.html', locals())


def index(request):
    return render(request, 'index.html', locals())

def about(request):
    
    return render(request, 'about.html', locals())

def update_history_data(request):
    th = threading.Thread(target=update_history,  name="update_history")
    th.start()
    return HttpResponse("<h1>Updateing history data.</h1>")


def update_history():
    Daily_transaction_information.objects.all().delete()
    Stock_name.objects.all().delete()
    Daily_transaction_information.objects.all().delete()
    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data"
    data = [row.split(',') for row in requests.get(url).text.splitlines()[1:]]
    # get stock name
    for r in data:
        item = Stock_name(
            stock_id=r[0][1:-1],
            name= r[1][1:-1]
        )
        item.save()
    for r in data:
        data = yf.download(f"{r[0][1:-1]}.TW", start="2022-5-1", end=str(datetime.date.today()))
        for index, row in data.iterrows():
            new_item = Daily_transaction_information(
                stock_id=r[0][1:-1],
                TradeVolume=row[5],
                date = pd.to_datetime(index).date(),
                HighestPrice=row[1],
                LowestPrice=row[2],
                ClosingPrice=row[3]
            )
            new_item.save()
        print(f"{r[0][1:-1]}.TW update.")
        time.sleep(10)

def update(request):

    url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY_ALL?response=open_data"
    data = [row.split(',') for row in requests.get(url).text.splitlines()[1:]]
    Stock_name.objects.all().delete()
    for r in data:
        item = Stock_name(
            stock_id=r[0][1:-1],
            name= r[1][1:-1]
        )
        item.save()
        
        # no data
        if r[5] == '""' or r[6] == '""' or r[7] == '""':
            continue
        new_data = Daily_transaction_information(
            stock_id=r[0][1:-1],
            TradeVolume = int(r[2][1:-1]),
            HighestPrice=float(r[5][1:-1]),
            LowestPrice=float(r[6][1:-1]),
            ClosingPrice=float(r[7][1:-1]),
            date= datetime.date.today()
        )
        new_data.save()

    return HttpResponse("<h1>updte stock data</h1>")

def test(request):
    return render(request, 'test.html', locals())
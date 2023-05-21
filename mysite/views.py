import datetime

from django.shortcuts import render
import requests, json
from django.http import HttpResponse
from mysite.models import *
# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

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
        # new_data = Daily_transaction_information(
        #     stock_id=r[0][1:-1],
        #     TradeVolume = int(r[2][1:-1]),
        #     HighestPrice=float(r[5][1:-1]),
        #     LowestPrice=float(r[6][1:-1]),
        #     ClosingPrice=float(r[7][1:-1]),
        #     date= datetime.date.today()
        # )
        # new_data.save()


    # name_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_P"
    # data = json.loads(requests.get(name_url).text)
    # Stock_name.objects.all().delete()
    # for d in data:
    #     new_item = Stock_name(
    #         stock_id=d["公司代號"],
    #         name=d["公司名稱"]
    #     )
    #     new_item.save()
    # name_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    # data = json.loads(requests.get(name_url).text)
    # for d in data:
    #     new_item = Stock_name(
    #         stock_id=d["公司代號"],
    #         name=d["公司名稱"]
    #     )
    #     new_item.save()
    #
    # print("update stock_name")
    return HttpResponse("<h1>updte stock data</h1>")
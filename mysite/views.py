from django.shortcuts import render
import requests, json
from django.http import HttpResponse
from mysite.models import *
# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

def update(request):
    name_url = "https://openapi.twse.com.tw/v1/opendata/t187ap03_L"
    data = json.loads(requests.get(name_url).text)
    Stock_name.objects.all().delete()
    for d in data:
        new_item = Stock_name(
            stock_id=d["公司代號"],
            name=d["公司名稱"]
        )
        new_item.save()
    print("update stock_name")
    return HttpResponse("<h1>updte stock data</h1>")
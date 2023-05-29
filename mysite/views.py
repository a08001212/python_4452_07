import datetime
import threading
import time
import numpy as np
from FinMind import strategies
from FinMind.data import DataLoader
from FinMind.strategies.base import Strategy
from ta.momentum import StochasticOscillator
import pandas as pd
import yfinance as yf
from mysite.average import *
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
                OpeningPrice=row[0],
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
            date= datetime.date.today(),
            OpeningPrice=float(r[4][1:-1])
        )
        new_data.save()

    return HttpResponse("<h1>updte stock data</h1>")

def test(request):
    return render(request, 'test.html', locals())

def Kd(request):
    data_loader = DataLoader()
    # data_loader.login('CHUN', 'kaikai8243') # 可選
    obj = strategies.BackTest(
        stock_id="0056",
        start_date="2018-01-01",
        end_date="2019-01-01",
        trader_fund=1000000.0,
        fee=0.001425,
        data_loader=data_loader,
    )

    class getKd(Strategy):
        kdays = 9
        kd_upper = 80
        kd_lower = 20

        def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
            stock_price = stock_price.sort_values("date")
            kd = StochasticOscillator(
                high=stock_price["max"],
                low=stock_price["min"],
                close=stock_price["close"],
                n=self.kdays,
            )
            rsv_ = kd.stoch().fillna(50)
            _k = np.zeros(stock_price.shape[0])
            _d = np.zeros(stock_price.shape[0])
            for i, r in enumerate(rsv_):
                if i == 0:
                    _k[i] = 50
                    _d[i] = 50
                else:
                    _k[i] = _k[i - 1] * 2 / 3 + r / 3
                    _d[i] = _d[i - 1] * 2 / 3 + _k[i] / 3
            stock_price["K"] = _k
            stock_price["D"] = _d
            stock_price.index = range(len(stock_price))
            stock_price["signal"] = 0
            stock_price.loc[stock_price["K"] <= self.kd_lower, "signal"] = 1
            stock_price.loc[stock_price["K"] >= self.kd_upper, "signal"] = -1
            return stock_price

    obj.add_strategy(Kd)
    obj.simulate()
    trade_detail = obj.trade_detail
    final_stats = obj.final_stats
    final_stats.rename(index={'MeanProfit': '中間收益',
                              'MaxLoss': '最大損失',
                              'FinalProfit': '最終收益',
                              'MeanProfitPer': '每股中間收益',
                              'FinalProfitPer': '每股最終收益',
                              'MaxLossPer': '每股最大損失',
                              'AnnualReturnPer': '每股年利潤',
                              'AnnualSharpRatio': '年夏普比率'}, inplace=True)
    print(final_stats)

    # print(obj.plot())
    trade_detail.rename(columns={'stock_id': '股票代碼',
                                 'date': '日期',
                                 'EverytimeProfit': '當下獲利',
                                 'RealizedProfit': '已實現損益',
                                 'UnrealizedProfit': '未實現損益',
                                 'hold_cost': '持有成本(股)',
                                 'hold_volume': '持有股數',
                                 'trade_price': '成交價格',
                                 'trader_fund': '交易資金'}, inplace=True)


    return trade_detail.values.tolist()

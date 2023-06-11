import datetime
import threading
import time
from typing import Any
import numpy as np
from pandas import Series, DataFrame
from ta.momentum import StochasticOscillator
import pandas as pd
import yfinance as yf
from mysite.average import *
from django.shortcuts import render
import requests, json
from django.http import HttpResponse
from mysite.models import *
from FinMind import strategies
from FinMind.data import DataLoader
from FinMind.strategies.base import Strategy
from ta.trend import SMAIndicator

# Create your views here.
def stockAnalysis(request):
    details = Stock_profit_rates.objects.all()
    return render(request, 'stockAnalysis.html', locals())

def backtesting(request):
    nDate = str(time.strftime("%Y-%m-%d", time.localtime()) )
    stocks = Stock_name.objects.all()
    details = []
    profit = 0.1
    try:
        strategy = request.GET['strategy']
        id = request.GET['id']
        sDate = request.GET['sDate']
        eDate = request.GET['eDate']
        fund = request.GET['fund']
                

        if strategy == 'strategy 1':
                profit, details = Kd(id, sDate, eDate, fund)
        elif strategy == 'strategy 2':
            profit, details = Bisa(id, sDate, eDate, fund)
    except:
         print("request.GET has wrong")
    TableBool = len(details) > 0

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

def moreBacktesting(request):
    nDate = str(time.strftime("%Y-%m-%d", time.localtime()) )
    stocks = Stock_name.objects.all()
    details = []
    profit = 0.1
    chooseStockDatas = "None"
    chooseStocks = ""

    if "id" in request.POST:
        id = request.POST['id']
        chooseStockDatas = "{},{}".format(str(request.POST["chooseStocks"]), str(id))
        chooseStocks = set(chooseStockDatas.split(","))
        chooseStocks.discard("None")
        chooseStocks = sorted(list(chooseStocks))
    if "fund" in request.POST and "chooseStocks" in request.POST and request.POST["chooseStocks"] != "None":
        strategy = request.POST['strategy']
        sDate = request.POST['sDate']
        eDate = request.POST['eDate']
        fund = request.POST['fund']
        chooseStockDatas = str(request.POST["chooseStocks"])
        chooseStocks = set(chooseStockDatas.split(","))
        chooseStocks.discard("None")
        chooseStocks = sorted(list(chooseStocks))

        profits = []
        detailses = []
        
        print("good")
        for id in chooseStocks:
            print("good")
            if strategy == 'strategy 1':
                profit, details = Kd(id, sDate, eDate, fund)
            elif strategy == 'strategy 2':
                profit, details = Bisa(id, sDate, eDate, fund)
            
            profits.append(profit)
            detailses.append([id, details])
    else:
         print("test1")
    TableBool = len(details) > 0
    
    # test = {"chooseStcks" : chooseStocks}
    # for x, y in test.items():
    #     print("{} : {}".format(x, y))

    return render(request, 'moreBacktesting.html', locals())

def update_profit_rates(request):
    Stock_profit_rates.objects.all().delete()
    eDate = str(datetime.datetime.now())[0:10]
    index = 0

    for s in Stock_name.objects.all():
        try:
            index += 1
            if(index % 70 == 0):
                time.sleep(3600)

            item = Stock_profit_rates(
                stock_id=s.stock_id,
                name= s.name,
                kd_profit_rate = Kd(s.stock_id, "2020-01-01", eDate, 100000, 1),
                bias_profit_rate = Bisa(s.stock_id, "2020-01-01", eDate, 100000, 1)
            )
            item.save()
            print("data" + str(index))
        except:
            continue

    return HttpResponse("<h1>updte stock profit_rates</h1>")

def Kd(id, sDate, eDate, fund, mode=0):
    data_loader = DataLoader()
    data_loader.login('CHUN', 'kaikai8243')  # 可選
    obj = strategies.BackTest(
        stock_id=id,
        start_date=sDate,
        end_date=eDate,
        trader_fund=int(fund),
        fee=0.001425,
        data_loader=data_loader,
    )
    # print("資料存取正常")

    '''
    Kd 隨機指標:
    是技術分析中的一種動量分析方法，採用超買和超賣的概念，由喬治·萊恩在1950年代推廣使用。指標通過比較收盤價格和價格的波動範圍，預測價格趨勢逆轉的時間。
    進出場策略:
    日K線 < 20 進場，> 80 出場
    '''

    class KD(Strategy):
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


    obj.add_strategy(KD)
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
    # print(final_stats)
    # print("中間測試")
    trade_detail.rename(columns={'stock_id': '股票代碼',
                                 'date': '日期',
                                 'EverytimeProfit': '當下獲利',
                                 'RealizedProfit': '已實現損益',
                                 'UnrealizedProfit': '未實現損益',
                                 'hold_cost': '持有成本(股)',
                                 'hold_volume': '持有股數',
                                 'trade_price': '成交價格',
                                 'trader_fund': '交易資金'}, inplace=True)
    trade_detail: Series | DataFrame | Any = trade_detail[
        ['股票代碼', '日期', '當下獲利', '已實現損益', '未實現損益', '持有成本(股)', '持有股數', '成交價格', '交易資金']]
    # return trade_detail.values.tolist()
    if mode == 0:
        return final_stats.values.tolist()[-2], trade_detail.values.tolist()
    else:
        return final_stats.values.tolist()[-2]

def Bisa(id, sDate, eDate, fund, mode=0):
    data_loader = DataLoader()
    data_loader.login('CHUN', 'kaikai8243')  # 可選
    obj = strategies.BackTest(
        stock_id=id,
        start_date=sDate,
        end_date=eDate,
        trader_fund=int(fund),
        fee=0.001425,
        data_loader=data_loader,
    )

    '''
    乖離率策略是觀察股價偏離移動平均線(MA線)的程度來決定是否進場
            負乖離表示股價 低 於過去一段時間平均價，意味著股價相對過去 低 ，所以選擇進場
            正乖離表示股價 高 於過去一段時間平均價，意味著股價相對過去 高 ，所以選擇出場
    進出場策略:
    負乖離 < -7，出場。正乖離 > 8，進場。
    '''

    class BIAS(Strategy):
        ma_days = 24
        bias_lower = -7
        bias_upper = 8

        def create_trade_sign(self, stock_price: pd.DataFrame) -> pd.DataFrame:
            stock_price = stock_price.sort_values("date")
            stock_price[f"ma{self.ma_days}"] = SMAIndicator(
                stock_price["close"], self.ma_days
            ).sma_indicator()
            stock_price["bias"] = (
                                          (stock_price["close"] - stock_price[f"ma{self.ma_days}"])
                                          / stock_price[f"ma{self.ma_days}"]
                                  ) * 100
            stock_price = stock_price.dropna()
            stock_price.index = range(len(stock_price))
            stock_price["signal"] = stock_price["bias"].map(
                lambda x: 1
                if x < self.bias_lower
                else (-1 if x > self.bias_upper else 0)
            )

            stock_price["signal"] = stock_price["signal"].fillna(0)
            return stock_price

    obj.add_strategy(BIAS)
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
    trade_detail.rename(columns={'stock_id': '股票代碼',
                                 'date': '日期',
                                 'EverytimeProfit': '當下獲利',
                                 'RealizedProfit': '已實現損益',
                                 'UnrealizedProfit': '未實現損益',
                                 'hold_cost': '持有成本(股)',
                                 'hold_volume': '持有股數',
                                 'trade_price': '成交價格',
                                 'trader_fund': '交易資金'}, inplace=True)
    trade_detail = trade_detail[
        ['股票代碼', '日期', '當下獲利', '已實現損益', '未實現損益', '持有成本(股)', '持有股數', '成交價格',
         '交易資金']]
    if mode == 0:
        return final_stats.values.tolist()[-2], trade_detail.values.tolist()
    else:
        return final_stats.values.tolist()[-2]
from django.db import models

# Create your models here.
class Stock_name(models.Model):
    stock_id = models.CharField(max_length=10, default="0")
    name = models.CharField(max_length=100, default="undef")


class Daily_transaction_information(models.Model):
    stock_id = models.CharField(max_length=10, default="0")
    date = models.DateField(auto_now=True)
    TradeVolume = models.IntegerField(default=0) #交易量
    HighestPrice = models.FloatField(default=0.0)
    LowestPrice = models.FloatField(default=.0)
    ClosingPrice = models.FloatField(default=.0) #收盤
    OpeningPrice = models.FloatField(default=.0)
    # MA5 MA10 MA20

class Stock_profit_rates(models.Model):
    stock_id = models.CharField(max_length=10, default="0")
    name = models.CharField(max_length=100, default="undef")
    kd_profit_rate = models.FloatField(default=0.0)
    bias_profit_rate = models.FloatField(default=0.0)
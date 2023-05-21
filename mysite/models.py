from django.db import models

# Create your models here.
class Stock_name(models.Model):
    stock_id = models.CharField(max_length=10, default="0")
    name = models.CharField(max_length=100, default="undef")


class Daily_transaction_information(models.Model):
    stock_id = models.CharField(max_length=10, default="0")
    date = models.DateField(auto_now=True)
    TradeVolume = models.IntegerField() #交易量
    HighestPrice = models.FloatField(default=0.0)
    LowestPrice = models.FloatField(default=.0)
    ClosingPrice = models.FloatField(default=.0) #收盤
    # MA5 MA10 MA20


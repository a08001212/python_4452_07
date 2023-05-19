from django.db import models

# Create your models here.
class Stock_name(models.Model):
    stock_id = models.IntegerField()
    name = models.CharField(max_length=100, default="undef")


class Daily_transaction_information(models.Model):
    stock_id = models.ForeignKey(Stock_name, on_delete=models.CASCADE)
    date = models.DateField()
    TradeVolume = models.IntegerField() #交易量
    HighestPrice = models.FloatField(default=0.0)
    LowestPrice = models.FloatField(default=.0)
    ClosingPrice = models.FloatField(default=.0) #收盤


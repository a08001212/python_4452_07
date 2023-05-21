from django.contrib import admin
from mysite import models         # 從mysite資料夾底下匯入models.py裡面所有的類別

# Register your models here.
admin.site.register(models.Stock_name)
admin.site.register(models.Daily_transaction_information)


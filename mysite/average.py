from mysite.models import *
import datetime
def get_average(stock_id: str, start: datetime.date, end: datetime.date)-> float:
    obj = Daily_transaction_information.objects.filter(stock_id__exact = stock_id, date__gte=start, date__lte=end)
    s = set()
    sum = .0
    for d in obj:
        if d.date in s:
            continue
        s.add(d.date)
        sum += d.ClosingPrice
    return sum /len(s)


from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html', locals())

def about(request):
    stock_ids = []
    return render(request, 'about.html', locals())
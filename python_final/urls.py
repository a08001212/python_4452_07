"""
URL configuration for python_final project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mysite import views

urlpatterns = [
    path('', views.index),
    path('index/', views.index),
    path('q&a/', views.qa),
    path('about/', views.about),
    path('backtesting/', views.backtesting),
    path('stockAnalysis/', views.stockAnalysis),
    path('test/', views.test),
    path('update/', views.update),
    path('admin/', admin.site.urls),
    path('update_history_data/', views.update_history_data),
    path('update_profit_rates/', views.update_profit_rates),
    path('moreBacktesting/', views.moreBacktesting),
]

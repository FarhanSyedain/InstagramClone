from django.shortcuts import render
from django.urls import path
from django.contrib import admin

from Home.views import test_home_template as home 
from Home.views import test_chat_main_template as chat_main
from Home.views import test_detail as detail


urlpatterns = [
    path('admin/',admin.site.urls),
    
    #These are temporary paths
    path('',home),
    path('chat',chat_main),
    path('detail',detail)
]


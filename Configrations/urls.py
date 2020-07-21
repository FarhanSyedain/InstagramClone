from django.shortcuts import render
from django.urls import path
from django.contrib import admin
from Home.views import test_home_template as home 
from Home.views import test_chat_main_template as chat_main
from Home.views import test_detail as detail
from Home.views import test_not as notification , test_profile as profile, posts ,test_detail_post as post_detail,test_ff

urlpatterns = [
    path('admin/',admin.site.urls),
    
    #These are temporary paths
    path('',home),
    path('chat',chat_main),
    path('detail',detail),
    path('notification',notification),
    path('profile',profile),
    path('post',posts),
    path('detail_post',post_detail),
    path('followers_following',test_ff),
]


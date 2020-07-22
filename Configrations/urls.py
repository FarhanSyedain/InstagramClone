from django.shortcuts import render
from django.urls import path
from django.contrib import admin
from Home.views import test_home_template as home 
from Home.views import test_chat_main_template as chat_main
from Home.views import test_detail as detail
from Home.views import test_not as notification , test_profile as profile, posts ,test_detail_post as post_detail,test_ff
from django.conf.urls.static import static
from django.conf import settings
from InstagramClone.settings import DEBUG


#Real imports
from Others import views as Others


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
    path('edit',test_ff),
    
    
    #Real paths
    
    path('<str:username>/',Others.profile_page,name='profile_page'),
    path('profile/api/get/data/posts/',Others.get_posts,name='API_get_posts')
    
    
    
]

if DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


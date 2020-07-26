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
    
    
    
    
    #API paths
    path('profile/api/get/data/posts/',Others.get_posts,name='API_get_posts'),
    path('profile/api/get/data/tagged/posts/',Others.get_tagged,name='API_get_posts'),
    path('profile/api/get/data/bookmarks/posts/',Others.get_bookmarks,name='API_get_book_marks'),
    path('profile/api/get/data/following/users/',Others.get_following,name='API_get_following'),
    path('profile/api/get/data/followers/users/',Others.get_followers,name='API_get_followers'),
    path('profile/api/get/data/remove/following/',Others.remove_following,name='API_remove_following'),
    path('profile/api/get/data/remove/follower/',Others.remove_followers,name='API_remove_follower'),
    path('profile/api/get/data/get/following/count',Others.get_following_count,name='API_get_following_count'),
    path('profile/api/get/data/get/followers/count',Others.get_followers_count,name='API_get_followers_count'),
    
    
]




if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


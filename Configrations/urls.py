from django.shortcuts import render
from django.urls import path
from django.contrib import admin
from Home.views import test_chat_main_template as chat_main
from Home.views import test_detail as detail
from Home.views import test_not as notification , test_profile as profile, posts , friend_requests
from django.conf.urls.static import static
from django.conf import settings
from InstagramClone.settings import DEBUG


#Real imports
from Profile import views as Profile
from Functionalities import views as Utilts
from Posts.views import post_detail
from Home import views as Home
from Posts import views as Post
from auth import views as Auth


urlpatterns = [
    path('admin/',admin.site.urls),
    
    #These are temporary paths
    path('',Home.home_page,name='home_page'),
    
    path('chat',chat_main),
    path('detail',detail),
    path('notification',notification),
    path('profile',profile),
    path('post',posts),
    path('post/<str:post_id>',post_detail),
    path('edit',Home.edit_profile,name='update_profile'),
    path('friend/requests',friend_requests),
    path('home/story',Home.story),
    
    
    #Real paths
    
    path('<str:username>/',Profile.profile_page,name='profile_page'),
    
    
    
    
    #API paths
    path('profile/api/get/data/posts/',Profile.get_posts,name='API_get_posts'),
    path('profile/api/get/data/tagged/posts/',Profile.get_tagged,name='API_get_posts'),
    path('profile/api/get/data/bookmarks/posts/',Profile.get_bookmarks,name='API_get_book_marks'),
    path('profile/api/get/data/following/users/',Profile.get_following,name='API_get_following'),
    path('profile/api/get/data/followers/users/',Profile.get_followers,name='API_get_followers'),
    path('profile/api/get/data/remove/following/',Profile.remove_following,name='API_remove_following'),
    path('profile/api/get/data/remove/follower/',Profile.remove_followers,name='API_remove_follower'),
    path('profile/api/get/data/get/following/count',Profile.get_following_count,name='API_get_following_count'),
    path('profile/api/get/data/get/followers/count',Profile.get_followers_count,name='API_get_followers_count'),
    path('profile/api/get/data/get_yourself',Profile.get_yourself,name='API_get_yourself'),
    path('profile/api/update_yourself',Profile.update_profile,name='API_update_yourself'),
    
    
    
    
    path('genral/api/follow/user',Utilts.follow_user,name='API_follow_user'),
    path('genral/api/unfollow/user',Utilts.unfollow_user,name='API_unfollow_user'),
    path('genral/api/delete/follow-request',Utilts.delete_request,name='API_delete_request'),
    path('genral/api/add_bookmark',Utilts.add_book_mark,name='API_add_book_mark'),
    path('genral/api/remove_bookmark',Utilts.remove_book_mark,name='API_remove_book_mark'),
    path('genral/api/like_post',Utilts.like_post,name='API_like_post'),
    path('genral/api/unlike_post',Utilts.unlike_post,name='API_unlike_post'),
    path('genral/api/add_comment_globally',Utilts.add_comment_globally,name='API_add_comment_globally'),
    
    
    path('post/api/reply_to_comment',Post.reply_to_comment,name='API_add_comment_locally'),
    path('post/api/delete_post',Post.delete_post,name='API_delete_post'),
    path('post/api/get/data/comments',Post.get_comments,name='API_get_comments'),
    path('post/api/get/data/comment/replies',Post.load_comment_replies,name='API_get_comment_replies'),
    
    path('friend_reqs/data/get',Utilts.get_follow_requests),
    path('friend_reqs/reject',Utilts.reject_request),
    path('friend_reqs/accept',Utilts.accept_request),
    
    
    path('home/api/get/data/posts',Home.get_posts,name='API_get_posts'),

    path('auth/login',Auth.login_user,name='Login'),
    path('auth/register',Auth.register_user,name='register'),
    path('auth/logout',Auth.logout_user,name='Logout'),
    
]




if DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    


from django.shortcuts import render,get_object_or_404,redirect
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from Configrations.models import *

from itertools import chain
from operator import attrgetter



def home_page(request):
    
 
    
    return render(request,'main/home.htm',)

@api_view(['POST'])
def get_posts(request):
    
    user = request.user.profile 
    all_following = Following.objects.get(user=user.user).following.all()
    
    all_posts = Post.objects.filter(user=user)
    
    querysets = [all_posts]
    
    for user_profile in all_following:
        querysets.append(Post.objects.filter(user=user_profile))
        
    all_posts = sorted(chain(*querysets),key=attrgetter('created'),reverse=True)
        
    data = request.data
    total_recived = data['recived']
    objs_per_call = data['per_call']
    
    if len(list(all_posts)) == 0:
        return Response({'proceed':False})
    
    try:
        some_posts = {}

        for post in list(all_posts)[total_recived:total_recived+objs_per_call]:
            like_count = post.likes.all().count()
            comment_count = Comment.objects.filter(post=post).count()
            is_bookmarked = BookMark.objects.get(user=request.user.profile).bookmarked_posts.all().filter(id=post.id).exists() 
            is_liked = post.likes.filter(username=request.user).exists()
            post_url = post.photo.url
            post_author = post.user.username
            post_caption = post.caption
            post_posted = post.created
            post_posted = str(post_posted)[:10]
            
            some_posts.update({post.id:[like_count,comment_count,is_bookmarked,post_url,is_liked,post_author,post_caption,post_posted]})

        try:
            has_more = True
            assert len(list(all_posts)[total_recived:total_recived+objs_per_call+1]) > 0
            
        except AssertionError:
            has_more = False
            
        to_be_returned = {'posts':some_posts,'others':{'has_more':has_more,'deleverd':len(list(all_posts)[total_recived:total_recived+objs_per_call])},'proceed':True}
 
        return Response(to_be_returned)
        
    except IndexError:

        some_posts = {}
        for post in list(all_posts)[total_recived:]:
            
            like_count = post.likes.all().count()
            comment_count = Comment.objects.filter(post=post).count()
            is_bookmarked = BookMark.objects.get(user=request.user.profile).bookmarked_posts.all().filter(id=post.id).exists() 
            post_url = post.photo.url
            post_author = post.user.username
            post_caption = post.caption
            is_liked = post.likes.filter(username=request.user).exists()
            post_posted = post.created
            post_posted = str(post_posted)[:10]
            some_posts.update({post.id:[like_count,comment_count,is_bookmarked,post_url,is_liked,post_author,post_caption,post_posted]})
            
        to_be_returned = {'posts':some_posts,'others':{'has_more':False,'deleverd':len(list(all_posts)[total_recived:])},'proceed':True}
        
        return Response(to_be_returned)
    







































































def test_chat_main_template(request):
    return render(request,'chat/main.htm')

def test_detail(request):
    return render(request,'chat/detail.htm')

def test_not(request):
    return render(request,'notification/notification.htm')

def test_profile(request):
    return render(request,'profile/profile.htm')

def posts(request):
    return render(request,'posts.htm')

def test_detail_post(request):
    return render(request,'main/post_detail.htm')


def edit_profile(request):
    
    username = request.user.username 
    first_name = '' if request.user.profile.first_name is None else request.user.profile.first_name
    last_name = '' if request.user.profile.last_name is None else request.user.profile.first_name
    phonenumber = '' if request.user.profile.phone_number is None else request.user.profile.phone_number
    Country = request.user.profile.country
    Country =  None if len(Country) == 0 else Country
    bio = '' if request.user.profile.bio is None else request.user.profile.bio
    countrys = ['Pakistan','Canada']
    
    private = request.user.profile.is_private
    
    content = {
        'username':username,'first_name':first_name,'last_name':last_name,'country':Country,'countrys':countrys,
        'phonenumber':phonenumber,'private':private,'bio':bio
    }
    
    return render(request,'profile/edit_profile.htm',content)


def friend_requests(request):
    return render(request,'main/friend_requests.htm')

def story(request):
    return render(request,'story.htm')



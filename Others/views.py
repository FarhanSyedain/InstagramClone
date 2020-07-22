from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse

import json


from Configrations.models import Post,Followers,Following,Profile

from rest_framework.decorators import api_view

# Main Profile page
def profile_page(request,username):
    
    if not request.user.is_authenticated or str(request.user) != username:
        
        user = get_object_or_404(Profile,username=username)
        is_owner = False
        is_private = user.is_private
        
        total_followers = Followers.objects.all().get(user=user.user).get_count
        total_following = Following.objects.all().get(user=user.user).get_count
        
        total_posts = Post.objects.all().filter(user=user).count()
        
        user_follows = is_following(request.user,user)
        
        profile_user_follows = is_following(user.user,request.user.profile)
            
        show = True if user_follows or not is_private else False
    
        context = {
            'user':user,'is_owner':is_owner,'is_private':is_private,'total_following':total_following,'total_posts':total_posts,
            'user_follows':user_follows,'profile_user_follows':profile_user_follows,'total_followers':total_followers,'show':show
        }
        
        return render(request,'profile/profile.htm',context)
    

    elif str(request.user) == username:
        
        user = get_object_or_404(Profile,username=username)
        is_owner = True
        
        total_followers = Followers.objects.all().get(user=user.user).get_count
        total_following = Following.objects.all().get(user=user.user).get_count
        
        total_posts = Post.objects.all().filter(user=user).count()
        
        show = True
        
        content = {
            'user':user,'is_owner':is_owner,'total_following':total_following,'total_posts':total_posts,'total_followers':total_followers,
            'show':show
        }
        
        return render(request,'profile/profile.htm',content)
    




def get_followers(request):
    pass




@api_view(['GET'])
def get_posts(request):
    
    data = json.loads(request.body)
        
    user = data['user']
    
    posts = Post.objects.all(user=user.profile)
    
    if len(posts) == 0:
        return JsonResponse({'last':True,'posts':None})
    
    
    if len(posts) < 4:
        
        to_be_returned = {
            'posts':posts,
            'last':True,
        }
        
        return JsonResponse(to_be_returned)
    
    
    
    else:
        deliverd_count = data['deliverd_count']
        
        posts_to_be_returned = posts[deliverd_count:deliverd_count+4]
        
        to_be_returned = {
            'posts':posts_to_be_returned,
            'last':False,
        }
        
        return JsonResponse(to_be_returned)
            
        

def get_bookmarks(request):
    pass


def get_following(request):
    pass

def get_tagged(request):
    pass



def is_following(user,whom):
    """
    Returns True if 'user' follows 'whom' and False if 'user' is not authenticated \n
    or does'nt follow 'whom'. User must be a user instance and whom must be a Profile instance
    """
    
    if not user.is_authenticated:
        return False
    
    following_obj = Following.objects.get(user=user)
    
    if following_obj.following.all().filter(username=whom.username).exists():
        return True
    return False
    


from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponseBadRequest

from Configrations.models import Post,Followers,Following,Profile,User,Tagged,BookMark
from Configrations.utilts import remove_follower

from rest_framework.response import Response
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
        
        profile_user_follows = is_following(user.user,request.user)
            
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
    

@api_view(['GET','POST'])
def get_posts(request):#For posts of user in User Profile
    """Returns Posts of a specific user.\n
    Designed for Profile Page"""
    
    data = request.data
    
    user = data['user']
    deliverd = data['total_recived']
    
    user_profile = Profile.objects.all().get(username=user)
    all_posts = Post.objects.all().filter(user=user_profile)

    posts_per_req = data['posts_per_call']
    
    if len(all_posts) == 0:
        return JsonResponse({'others':{'last':True,'has_posts':False}},safe=False)
    else:
       try: 
            posts = {}
            for post in all_posts[deliverd:deliverd+posts_per_req]:
                posts.update({f'{post}':[f'{post.id}',f'{post.photo.url}']})
            try:
                if len(all_posts) <= deliverd+1:
                    raise IndexError
                last = False
            except IndexError:
                last = True
                                
            other_values = {'last':last,'has_posts':True}

            to_be_returned = {'posts':posts,'others':other_values} 
            
            return JsonResponse(to_be_returned,safe=False)
        
       except IndexError:
           
            posts = {}
            for post in all_posts[deliverd:]:
                posts.update({f'{post}':[f'{post.id}',f'{post.photo.url}']})
            
            other_values = {'last':True,'has_posts':True}

            to_be_returned = {'posts':posts,'others':other_values} 
            
            return JsonResponse(to_be_returned,safe=False)
   

@api_view(['GET','POST'])
def get_tagged(request):
    """Returns Posts in which user is tagged\n
    Designed for Profile Page"""
    
    data = request.data
    
    deliverd = data['total_deleverd']
    user = data['user']
    posts_per_call = data['posts_per_call']
        
    user_profile = Profile.objects.all().get(username=user)
    
    user_tagged_in = Tagged.objects.get(user=user_profile).tagged_in.all()

    if len(user_tagged_in) == 0:

        return JsonResponse({'is_tagged_in_any':False},safe=False)
    
    else:
        try:

            tagged_posts = {}
            for tagged_post in list(user_tagged_in)[deliverd:deliverd+posts_per_call]:
                tagged_posts.update({f'{tagged_post}':[f'{tagged_post.id}',f'{tagged_post.photo.url}']})

            has_more = True
            
            if len(user_tagged_in) <= deliverd+1:
                has_more = False
            
            others = {'has_more_tagged_posts':has_more}
            
            to_be_returned = {'tagged':tagged_posts,'others':others,'is_tagged_in_any':True}
            
            return JsonResponse(to_be_returned,safe=False)
        
        except IndexError:
            tagged_posts = {}
            for tagged_post in list(user_tagged_in)[deliverd:]:
                tagged_post.update({f'{tagged_post}':[f'{tagged_post.id}',f'{tagged_post.photo.url}']})

            others = {'has_more_tagged_posts':False}
            
            to_be_returned = {'tagged':tagged_posts,'others':others,'is_tagged_in_any':True}
            
            return JsonResponse(to_be_returned,safe=False)
        

@api_view(['GET','POST'])
def get_bookmarks(request):
    """Returns Images saved by a user\n
    Designed for profile page"""
    
    data = request.data
    
    deliverd = data['book_marks_recived']
    user_name = data['user']
    
    user_profile = Profile.objects.all().get(username=user_name)
    
    all_book_marks = BookMark.objects.all().get(user=user_profile).bookmarked_posts.all()
    
    if len(all_book_marks) == 0:
        return JsonResponse({'has_book_marks':False},safe=False)

    else:
        
        posts_per_call = data['posts_per_call']
        
        try:
            
            some_book_marks = {}
            
            for book_mark_obj in list(all_book_marks)[deliverd:deliverd+posts_per_call]:
                some_book_marks.update({f'{book_mark_obj}':[f'{book_mark_obj.id}',f'{book_mark_obj.photo.url}']})
            
            has_more = True
        
            if len(all_book_marks) <= (deliverd + 1):
                has_more = False

            others = {'has_more':has_more}
            
            return JsonResponse({'book_marks':some_book_marks,'others':others,'has_book_marks':True},safe=False)

        except IndexError:
            some_book_marks = {}
            
            for book_mark_obj in list(all_book_marks)[deliverd:]:
                some_book_marks.update({f'{book_mark_obj}':[f'{book_mark_obj.id}',f'{book_mark_obj.photo.url}']})

            return JsonResponse({'book_marks':some_book_marks,'others':{'has_more':False},'has_book_marks':True},safe=False)


@api_view(['POST','GET'])
def get_following(request):
    
    """Returns the users followed by the user -- To whom belongs the profile--\n
    Designed for profile page """
    
    data = request.data
    
    user = data['user']
    deliverd = data['deliverd']
    per_call = data['per_call']
    
    user = User.objects.get(username=user)
    
    following = Following.objects.get(user=user).following.all()
    
    if len(list(following)) == 0:
        return JsonResponse({'is_following_anyone':False},safe=False)
    
    else:
        try:
            users_following = {}
            for user_ in list(following)[deliverd:deliverd+per_call]:
                if not user_.first_name is None:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.profile_picture.url}',f'{user_.username}']})
                else:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.profile_picture.url}']})

            has_more = True
            
            if len(following) <= (deliverd + 1):
                has_more = False
                
            others = {'has_more':has_more,'deliverd':deliverd+len(list(following)[deliverd:])}
            to_be_returned = {'following':users_following,'is_following_anyone':True,'others':others}
            
            return JsonResponse(to_be_returned,safe=False)

        except IndexError:
            
            for user_ in list(following)[deliverd:]:
                if not user_.first_name is None:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.photo.profile_picture.url}',f'{user_.username}']})
                else:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.photo.profile_picture.url}']})
                    
                    
            others = {'has_more':False,'deliverd':deliverd+len(list(following)[deliverd:])}
            to_be_returned = {'following':users_following,'is_following_anyone':True,'others':others}
            
            return JsonResponse(to_be_returned,safe=False)


@api_view(['POST','GET'])
def get_followers(request):
    
    """Returns the users followed by the user -- To whom belongs the profile--\n
    Designed for profile page """
    
    data = request.data
    
    user = data['user']
    deliverd = data['deliverd']
    per_call = data['per_call']
    
    user = User.objects.get(username=user)
    
    followers = Followers.objects.get(user=user).followers.all()
    
    if len(list(followers)) == 0:
        return JsonResponse({'is_followed':False},safe=False)
    
    else:
        try:
            users_following = {}
            for user_ in list(followers)[deliverd:deliverd+per_call]:
                if not user_.first_name is None:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.profile_picture.url}',f'{user_.username}']})
                else:
                    users_following.update({f'{user_}':[f'{user_.id}',f'{user_.profile_picture.url}']})

            has_more = True
            
            if len(followers) <= (deliverd + 1):
                has_more = False
                
            others = {'has_more':has_more,'deliverd':deliverd+len(list(followers)[deliverd:deliverd+per_call])}
            to_be_returned = {'followers':users_following,'is_followed':True,'others':others}
            
            return JsonResponse(to_be_returned,safe=False)

        except IndexError:
            
            for user_ in list(followers)[deliverd:]:
                if not user_.first_name is None:
                    users_following.update({f'{user_}':[f'{user_.photo.profile_picture.url}',f'{user_.username}']})
                else:
                    users_following.update({f'{user_}':[f'{user_.photo.profile_picture.url}']})
                    
                    
            others = {'has_more':False,'deliverd':deliverd+len(list(followers)[deliverd:])}
            to_be_returned = {'following':users_following,'is_followed':True,'others':others}
            
            return JsonResponse(to_be_returned,safe=False)


@api_view(['POST','GET'])
def remove_following(request):
    
    data = request.data
    
    user_to_be_removed = data['username']
    to_be_removed_from = data['user']
    user = request.user
    if request.user.is_authenticated and str(user) == str(to_be_removed_from):
        
        user_to_be_removed = User.objects.get(username=user_to_be_removed)
        to_be_removed_from = User.objects.get(username=to_be_removed_from)
        
        removed_user = remove_follower(to_be_removed_from,user_to_be_removed)
        return JsonResponse({'success':removed_user,'id':Profile.objects.get(username=user_to_be_removed).id},safe=False)
        
    return HttpResponseBadRequest('Detected data minuplitaion')


@api_view(['POST','GET'])
def remove_followers(request):
    
    data = request.data
    
    user_to_be_removed = data['username']
    to_be_removed_from = data['user']
    user = request.user
    if request.user.is_authenticated and str(user) == str(to_be_removed_from):
        
        user_to_be_removed = User.objects.get(username=user_to_be_removed)
        to_be_removed_from = User.objects.get(username=to_be_removed_from)
        
        remove_user = remove_follower(to_be_removed_from,user_to_be_removed)
        return JsonResponse({'success':remove_user,'id':Profile.objects.get(username=user_to_be_removed).id},safe=False)

    return HttpResponseBadRequest('Detected data minuplitaion')




@api_view(['POST','GET'])
def get_following_count(request):
    
    data = request.data
    
    user = User.objects.get(username=data['user'])
    return JsonResponse({'count':Following.objects.get(user=user).following.count()},safe=False)


@api_view(['POST','GET'])
def get_followers_count(request):
    
    data = request.data
    
    user = User.objects.get(username=data['user'])
    return JsonResponse({'count':Followers.objects.get(user=user).followers.count()},safe=False)


def is_following(user,whom):
    """
    Returns True if 'user' follows 'whom' and False if 'user' is not authenticated \n
    or does'nt follow 'whom'. User must be a user instance and whom must be a Profile instance
    """

    if not user.is_authenticated:
        return False

    if isinstance(whom,User):
        if not whom.is_authenticated:
            return False

        whom = whom.profile
        
    following_obj = Following.objects.get(user=user)

    if following_obj.following.all().filter(username=whom.username).exists():
        return True
    return False
    

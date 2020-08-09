from Configrations.utilts import *
from Configrations.models import *

from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest

from rest_framework.response import Response

@api_view(['POST'])
def follow_user(request):
    """Follows or sends request to a user and returnes the button text --Followed or Requested"""
    
    data = request.data
    print(data['username'])
    user = Profile.objects.get(username=data['username'])
    
    if user.is_private:
        if not FollowRequestMassage.objects.all().filter(send_by=request.user,send_to=user).exists():
            req = FollowRequestMassage()
            req.send_by = request.user
            req.send_to = user
            req.save()
        return JsonResponse({'success':True,'Requested':True},safe=False)
    
    else:
        user_followed = follow_user_(user,request.user)
        if user_followed:
            if is_following(user,request.user):
                return JsonResponse({'success':True,'Requested':False,'Follows':True,'id':user.id},safe=False)
            return JsonResponse({'success':True,'Requested':False,'Follows':False,'id':user.id},safe=False)
            
        return JsonResponse({'success':False},safe=False)
    
    
@api_view(['POST'])
def unfollow_user(request):
    '''Unfollow User and then returns the button text and info'''
    
    data = request.data
    to_be_removed_from = request.user
    user_to_be_removed = Profile.objects.get(username=data['username'])
    user_unfollowed = remove_follower(to_be_removed_from,user_to_be_removed)
    
    if user_unfollowed:
        if is_following(user_to_be_removed,to_be_removed_from):
            return JsonResponse({'success':True,'Follows':True},safe=False)
        return JsonResponse({'success':True,'Follows':False},safe=False)
    
    return JsonResponse({'success':False},safe=True)


@api_view(['POST'])
def delete_request(request):
    """Deletes a Follow Request and returns the button text\n
    Note: It wont delete the notification that user -- whom follow req is send to -- will recive"""
    
    data = request.data
    user = Profile.objects.get(username=data['username'])
    req_deleted = delete_follow_request(request.user,user)
    
    if req_deleted:
        if is_following(user.user,request.user):
            return JsonResponse({'success':True,'Follows':True},safe=False)
        return JsonResponse({'success':True,'Follows':False},safe=False)
    
    return JsonResponse({'success':False},safe=False)
    

@api_view(['POST'])
def add_book_mark(request):
    try:
        data = request.data
        id_ = data['id']
        post = get_object_or_404(Post,id=id_)
        BookMark.objects.get(user=request.user.profile).bookmarked_posts.add(post)
        return Response({'success':True})
    except:
        pass
    

@api_view(['POST'])
def remove_book_mark(request):
    try:
        data = request.data
        id_ = data['id']
        post = get_object_or_404(Post,id=id_)
        BookMark.objects.get(user=request.user.profile).bookmarked_posts.remove(post)
        return Response({'success':True})
    except:
        pass


@api_view(['POST'])
def like_post(request):
    try:
        data = request.data
        id_ = data['id']
        post = get_object_or_404(Post,id=id_)
        post.likes.add(request.user)
        return Response({'success':True,'count':post.likes.all().count()})
    except:
        pass
    
    
@api_view(['POST'])
def unlike_post(request):
    try:
        data = request.data 
        id_ = data['id']
        post = get_object_or_404(Post,id=id_)
        post.likes.remove(request.user)
        return Response({'success':True,'count':post.likes.all().count()})
    except:
        pass
    
    
@api_view(['POST'])
def add_comment_globally(request):
    try:
        data = request.data
        user = request.user 
        comment_body = data['comment_body']
        post_id = data['post_id']
        
        post = Post.objects.get(id=post_id)
        comment = Comment()
        comment.comment_body = comment_body
        comment.post = post
        comment.author = request.user.profile
        comment.save()
        
        total_comments = Comment.objects.filter(post=post).count()
       
        return Response({'success':True,'total_comments':total_comments})
    except :
        return Response({'success':False})


@api_view(['POST'])
def get_follow_requests(request):
    
    data = request.data 
    deliverd = data['last']
    per_call = data['per_call']
    
    user = request.user.profile 
    
    all_requests = FollowRequests.objects.get(user=user).requests.all()
    
    if len(all_requests) == 0:
        return Response({'proceed':False})
    try:
        some_requests = []
        
        for req in list(all_requests)[deliverd:deliverd+per_call]:
            some_requests.append([req.send_by.profile.profile_picture.url,req.send_by.username])
        
        has_more = len(all_requests[deliverd+per_call:]) > 0
        
        return Response({'requests':some_requests,'has_more':has_more,'recived':len(list(all_requests)[deliverd:deliverd+per_call]),'proceed':True})
    
    except IndexError:
        some_requests = []
        
        for req in list(all_requests)[deliverd:]:
            
            some_requests.append([req.send_by.profile.profile_picture.url,req.send_by.username])
        
        return Response({'requests':some_requests,'has_more':False,'recived':len(list(all_requests)[deliverd:]),'proceed':True})
        

@api_view(['POST'])
def accept_request(request):
    
    username = request.data['username']
    
    user = request.user.profile
    try:
        if FollowRequestMassage.objects.filter(send_to=user,send_by=User.objects.get(username=username)).exists():
            FollowRequestMassage.objects.get(send_to=user,send_by=User.objects.get(username=username)).accept()
            return Response({'success':True})
            
        else:
            return Response({'success':True})
    except:
        return Response({'success':True})

    
    

@api_view(['POST'])
def reject_request(request):
    
    username = request.data['username']
    
    user = request.user.profile
    try:
        if FollowRequestMassage.objects.filter(send_to=user,send_by=User.objects.get(username=username)).exists():
            FollowRequestMassage.objects.get(send_to=user,send_by=User.objects.get(username=username)).reject()
            return Response({'success':True})
            
        else:
            return Response({'success':True})
    except:
        return Response({'success':True})






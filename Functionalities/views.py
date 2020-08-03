from Configrations.utilts import *
from Configrations.models import *
# Create your views here.

@api_view(['POST'])
def follow_user(request):
    """Follows or sends request to a user and returnes the button text --Followed or Requested"""
    
    data = request.data
    user = Profile.objects.get(username=data['username'])
    
    if user.is_private:
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
    
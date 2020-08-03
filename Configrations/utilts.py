from .models import Profile,Followers,Following,User,FollowRequestMassage
from django.http import JsonResponse

from rest_framework.decorators import api_view


def remove_follower(from_whom,who):
    
    """Unfollows 'who' from  'from_whom'\n
    Returns True if succeed,otherwise False  """
    
    try:

        from_whom = from_whom.user if isinstance(from_whom,Profile) else from_whom
        who = who.user if isinstance(who,Profile) else who

        follower_obj = Followers.objects.get(user=who)
        following_obj = Following.objects.get(user=from_whom)

        follower_obj.followers.remove(from_whom.profile)
        following_obj.following.remove(who.profile)

        follower_obj.save()
        following_obj.save()

    except:
        return False
    return True



def follow_user_(username,who_will_follow):
    
    """Follows username from who_will_follow.\n
    Returns True if successfully follows else returns False\n
    Parameters must be either user or profile instances"""

    try:
        
        username = username.user if isinstance(username,Profile) else username
        who_will_follow = who_will_follow.user if isinstance(who_will_follow,Profile) else who_will_follow
        
        followers_obj = Followers.objects.get(user=username)
        following_obj = Following.objects.get(user=who_will_follow)

        followers_obj.followers.add(who_will_follow.profile)
        following_obj.following.add(username.profile)

        following_obj.save()
        followers_obj.save()
        
        return True
    
    except:
        return False


def is_following(user,whom):
    """
    Returns True if 'user' follows 'whom' and False if 'user' is not authenticated
    or does'nt follow 'whom'. User must be a user instance and whom must be a Profile instance
    """

    whom = whom.profile if isinstance(whom,User) else whom

    user = user.user if isinstance(user,Profile) else user

    following_obj = Following.objects.get(user=user)

    if following_obj.following.all().filter(username=whom.username).exists():
        return True
    return False
    

def get_extra_info(user_,user):
    
    button_info_dict = {
        'CASEONE':['Follow','_follow_user(',f'{user_}'],
        'CASETWO':['Unfollow','_unfollow_user(',f'{user_}'],
        'CASETHREE':['Follow Back','_follow_user(',f'{user_}'],
        'CASEFOUR':['Requested','_del_req(',f'{user_}'],
        'IFIS':['','']
    }
    if str(user_) == str(user):
        return button_info_dict['IFIS']
    
    if is_following(user,user_):
        return button_info_dict['CASETWO']
    
    elif is_following(user_.user,user):
        return button_info_dict['CASETHREE']
    
    elif FollowRequestMassage.objects.all().filter(send_by=user,send_to=user_):
        return button_info_dict['CASEFOUR']
    
    else:
        return button_info_dict['CASEONE']
    

def delete_follow_request(send_by,send_to):
    """"Deletes a follow req and returns True if succeed or False if faild"""
    try:
        send_by = send_by.user if isinstance(send_by,Profile) else send_by
        send_to = send_to.profile if isinstance(send_to,User) else send_to
        
        FollowRequestMassage.objects.get(send_by=send_by,send_to=send_to).reject()
        return True
    
    except:
        return False
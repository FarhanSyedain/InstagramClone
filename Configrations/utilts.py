from .models import *


def remove_follower(from_whom,who):
    """Removes Follower of a specific user\n.
    Returns True if succeed else False"""
    try:
        from_whom = from_whom.user if isinstance(from_whom,Profile) else from_whom
        who = who.user if isinstance(who,Profile) else who

        follower_obj = Followers.objects.get(user=from_whom)
        following_obj = Following.objects.get(user=who)

        follower_obj.followers.remove(who.profile)
        following_obj.following.remove(from_whom.profile)

        
        follower_obj.save()
        following_obj.save()
    except Exception:
        return False
    
    return True

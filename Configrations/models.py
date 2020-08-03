from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.utils import timezone

#Profiles of everyone 
class Profile(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=25,null=True,blank=True)
    last_name = models.CharField(max_length=25,null=True,blank=True)
    username = models.CharField(max_length=40,null=True)
    is_private = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics',default='default/anon.png') #A default photo to be added in folder
    date_created = models.DateTimeField(auto_now_add=True)
    profile_updated_on = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=25,blank=True)
    bio = models.TextField(blank=True)
    
    
    def __str__(self):
        
        return (self.username if self.first_name is None else str(self.first_name + self.last_name))


class Post(models.Model):
    
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    photo = models.ImageField(upload_to='posts')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    @property
    def like_count(self):
        
        return self.likes.objects.all().count()
    
    
    @property
    def get_count(self):
        
        return Post.objects.filter(instance=self).count()
    class Meta:
        ordering = ['-id']
    

class Tagged(models.Model):

    user = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    tagged_in = models.ManyToManyField(Post,blank=True)    

class Post_Tags(models.Model):
    post = models.OneToOneField(Post,on_delete=models.CASCADE,null=True)
    tagged = models.ManyToManyField(User,blank=True)


class Comment(models.Model):
    
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    comment_body = models.TextField()
    
    
class Following(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True) 
    following = models.ManyToManyField(Profile,blank=True)
    
    @property
    def get_count(self):
        return self.following.count()

class Followers(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True) 
    followers = models.ManyToManyField(Profile,blank=True)

    @property
    def get_count(self):
        return self.followers.count()



class BookMark(models.Model):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    bookmarked_posts = models.ManyToManyField(Post,blank=True)


class FollowRequestMassage(models.Model):
    
    send_by = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    send_to = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    send_on = models.DateTimeField(auto_now_add=True)
    
    def accept(self):
        
        follower_obj = Followers.objects.get(user=self.send_to.user)
        following_obj = Following.objects.get(user=self.send_by)

        follower_obj.followers.add(self.send_by.profile)
        following_obj.following.add(self.send_to)

        follower_obj.save()
        following_obj.save()
        
        self.delete()
    

    def reject(self):
        
        self.delete()
        

    
    
    
class FollowRequests(models.Model):
    user = models.OneToOneField(Profile,on_delete=models.CASCADE,null=True)
    requests = models.ManyToManyField(FollowRequestMassage,blank=True)



def post_save__tagged(sender,instance,created,*args,**kwargs):
    if created:
        tagged_ = Post_Tags()
        tagged_.post = instance
        tagged_.save()
        
        
def create_user_(sender,instance,created,*args,**kwargs):
    if created:
        profile = Profile()
        profile.user = instance
        profile.username  = instance.username
        profile.save()
        
        follow_req = FollowRequests()
        follow_req.user = profile
        follow_req.save()
        
        follower_obj = Followers()
        follower_obj.user = profile.user
        follower_obj.save()
        
        following_obj = Following()
        following_obj.user = profile.user
        following_obj.save()
        
        bookmark_obj = BookMark()
        bookmark_obj.user = profile
        bookmark_obj.save()
        
        tagged_obj = Tagged()
        tagged_obj.user = profile
        tagged_obj.save()
        

def on_req_user(sender,instance,created,*args,**kwargs):
    if created:
        
        send_to = instance.send_to
        obj = FollowRequests.objects.get(user=instance.send_to)
        obj.requests.add(instance)
        obj.save()
             
             
post_save.connect(post_save__tagged,Post)
post_save.connect(create_user_,User)
post_save.connect(on_req_user,FollowRequestMassage)

all_objects_to_be_added_in_adminpage = [Comment,Post,Profile,Tagged,Following,Followers,Post_Tags,BookMark,FollowRequests,FollowRequestMassage]
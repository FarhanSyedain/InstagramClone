from django.db import models
from django.contrib.auth.models import User

#Profiles of everyone 
class Profile(models.Model):
    
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    first_name = models.CharField(max_length=25,null=True,blank=True)
    last_name = models.CharField(max_length=25,null=True,blank=True)
    username = models.CharField(max_length=40,null=True)
    is_private = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics',default='Anon.png') #A default photo to be added in folder
    date_created = models.DateTimeField(auto_now_add=True)
    profile_updated_on = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=15,blank=True)
    country = models.CharField(max_length=25,blank=True)
    bio = models.TextField(blank=True)
    
    
    def __str__(self):
        
        return (self.username if len(self.first_name) == 0 else str(self.first_name + self.last_name))


class Post(models.Model):
    
    user = models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    photo = models.ImageField(upload_to='posts')
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User,blank=True)
    
    @property
    
    def like_count(self):
        
        return self.likes.objects.all().count()
    
    @property
    def get_count(self):
        
        return Post.objects.filter(instance=self).count()
    
    

class Tagged(models.Model):
    
    post = models.ForeignKey(Post,on_delete=models.CASCADE,null=True)
    tagged_people = models.ManyToManyField(Profile,blank=True)
    
    

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


all_objects_to_be_added_in_adminpage = [Comment,Post,Profile,Tagged,Following,Followers]
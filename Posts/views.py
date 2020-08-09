"""This file is dedicated for post detail ; the functions that are required in post detail page"""

from django.shortcuts import render,get_object_or_404 
from django.http import HttpResponseBadRequest

from rest_framework.decorators import api_view
from rest_framework.response import Response

from Configrations.models import *
from Functionalities.views import is_following


def post_detail(request,post_id):
    
    post = get_object_or_404(Post,id=post_id)
    
    if post.user.is_private and not is_following(request.user,post.user):
        return HttpResponseBadRequest('This is a private account')
    
    book_marked = False
    liked_by_user = False
    
    if BookMark.objects.get(user=request.user.profile).bookmarked_posts.all().filter(id=post_id).exists():
        book_marked = True
    
    if post.likes.all().filter(username=request.user.profile.username).exists():
        liked_by_user = True
        
    
    comments_count = Comment.objects.all().filter(post=post).count()
    owner_pic_url =  '..' + str(post.user.profile_picture.url)
    uploaded_on = str(post.created)[:10] #Return only YY__MM__DD 
    post_url = '..' + str(post.photo.url)
    is_owner = str(request.user) == str(post.user) 
    
    
    content = {'id':post_id,'post_owner':post.user.username,'like_count':post.like_count,'is_book_marked':book_marked,'post_url':post_url,
               'total_comments':comments_count,'liked_by_user':liked_by_user,'owner_pic_url':owner_pic_url,'uploaded_on':uploaded_on,'is_owner':is_owner
               }
    
    return render(request,'main/post_detail.htm',content)


@api_view(['POST'])
def reply_to_comment(request):
    
    data = request.data
    user = request.user
    comment_body = data['comment_body']
    comment_id = data['id']
    
    try:
        comment = get_object_or_404(Comment,id=comment_id)
    except:
        return Response({'error_':True})        
    
    reply = CommentReply()
    reply.comment_body = comment_body
    reply.parent_comment = comment
    reply.author = request.user.profile 
    reply.save()
    reply_count = CommentReply.objects.filter(parent_comment=comment).count()
    
    return Response({'error':False,'reply_count':reply_count})


@api_view(['POST'])
def delete_post(request):
    try:
        user = request.user.profile
        data = request.data 
        post = get_object_or_404(Post,id=data['id'])
        
        if str(post.user.username) == str(user):
            post.delete()
            return Response({'success':True})
        return Response(status=403)
    except:
        return Response({'success':False})
    

@api_view(['POST'])
def get_comments(request):
    
    data = request.data
    post_id = data['id']
    post = get_object_or_404(Post,id=post_id)
    
    try:
        assert (proceed :=  Comment.objects.filter(post=post).exists()) #Check if we have comments.Incase you have python 3.7 or less,alter the code
    except AssertionError:
        return Response({'proceed':proceed})
    
    deliverd = data['deliverd']
    per_call = data['per_call']
    
    try:
        some_comments = []
        for comment in list(Comment.objects.filter(post=post))[deliverd:deliverd+per_call]:
            reply_count = CommentReply.objects.filter(parent_comment=comment).count()
            some_comments.append([f'{comment.comment_body}',f'{comment.author.username}',f'{comment.author.profile_picture.url}',f'{comment.dated}',f'{reply_count}',f'{comment.id}'])
        try:
            assert (has_more := len(Comment.objects.filter(post=post)[deliverd+per_call:])>0)
        except AssertionError:
            has_more = False
        
        return Response({'comments':some_comments,'has_more':has_more,'proceed':proceed,'recived':len(list(Comment.objects.filter(post=post))[deliverd:deliverd+per_call])})
        
    except IndexError:
        some_comments = []
        for comment in list(Comment.objects.filter(post=post))[deliverd:deliverd+per_call]:
            reply_count = CommentReply.objects.filter(parent_comment=comment).count()
            some_comments.append([f'{comment.comment_body}',f'{comment.author.username}',f'{comment.author.profile_picture.url}',f'{comment.dated}',reply_count,f'{comment.id}']) 
        
        return Response({'comments':some_comments,'has_more':False,'proceed':proceed,'recived':len(list(Comment.objects.filter(post=post))[deliverd:])})
            

@api_view(['POST'])
def load_comment_replies(request):
    
    data = request.data 
    
    deliverd = data['deliverd']
    per_call =  data['per_call']
    comment_id = data['id']
    
    try:
        assert (exists := Comment.objects.filter(id=comment_id).exists() )
    except AssertionError:
        return Response({'exists':False})
    
    all_replies = CommentReply.objects.filter(parent_comment=comment_id)
    
    try:
        some_replies = []
        for reply in list(all_replies)[deliverd:deliverd+per_call]:
            some_replies.append([f'{reply.comment_body}',f'{reply.author.username}',f'{reply.author.profile_picture.url}',f'{reply.dated}'])
        
        has_more = len(all_replies[deliverd+per_call:]) > 0
            
        return Response({'replies':some_replies,'has_more':has_more,'exists':True,'recived':len(list(all_replies)[deliverd:deliverd+per_call])})
    
    except IndexError:
        some_replies = []
        for reply in list(all_replies)[deliverd:]:
            some_replies.append([f'{reply.comment_body}',f'{reply.author.username}',f'{reply.author.profile_picture.url}',f'{reply.dated}'])
        
        return Response({'replies':some_replies,'has_more':False,'exists':True,'recived':len(list(all_replies)[deliverd:])})
        

    
    

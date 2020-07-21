from django.shortcuts import render


def test_home_template(request):
    return render(request,'main/home.htm')

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

def test_ff(request):
    return render(request,'profile/followers_folloiwing.htm')
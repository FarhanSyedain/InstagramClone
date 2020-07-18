from django.shortcuts import render


def test_home_template(request):
    return render(request,'main/home.htm')

def test_chat_main_template(request):
    return render(request,'chat/main.htm')

def test_detail(request):
    return render(request,'chat/detail.htm')

from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from Configrations.models import *

def login_user(request):
    incorrect_cred = False
    
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method ==  'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')

        if remember is None:
            pass #dont remember the user //Program later
        
        user = authenticate(request,username=username,password=password)
        
        if user is not None:
            login(request,user)
            try:
                return redirect(request.GET['next'])
            except:
                return redirect('home_page')
        
        incorrect_cred = True
    
    
    return render(request,'auth/login.htm',{'incorrect_cred':incorrect_cred})


def register_user(request):
    
    incorrect_email = False
    
    form = RegisterUser()
   
    if request.method == 'POST':
        
        username = request.POST.get('username')
        password = request.POST.get('password1')
 
        incorrect_email = False
        form = RegisterUser(request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(request,username=username,password=password)
            if not user is None:
                login(request,user)
                return redirect('update_profile')
            
    
    return render(request,'auth/register.htm',{'form':form,'incorrect_email':incorrect_email})
    

def logout_user(request):
    
    if not request.user.is_authenticated:
        return redirect('Login')
    
    logout(request)
    return redirect('Logout')

    
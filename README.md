InstagramClone
pip install Django
cd to BASE Dir and run   py manage.py runserver
Boom



 How and where to add A template and view and route
 Since we are coding frontend first,we will create all of our views in Home.views   then later change
 all templates in templaes folder -- Order then in subfolders if nesscery
 All urls in Configrations.urls 

 To create:
   Make a template first
       Make a view    
       def viewname(request):
           return(request,'TEMPLATELOC')

 Note TEMPLATE loc starts from templates folder so if you have created a sub folder in templates and a file in the
 subfolder as lets suppose u named it a.htm, then TEMPLATELOC will be nameofthesubfolder/a.htm

 add a url route
 path('Routeadress',view)  replace view with the view created in  home,views also u need to import that
 save all the fiels



 Jinja or Jings guide


 In our base template we have: A bottom fixed nav bar , and a boiler plate.

 If you want to add the bottom nav to the template then add the following lines of code to the template

 {%extends 'main.htm %}  
 {%load static %}
 {%block content %}
 All your code here      btw dont add a boiler pate 
 {%endblock%}



 to access the static folder    {% static 'path' %}    static folder contains   all the static stuuf
"""
URL configuration for blogproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from blogapp.views import * 


urlpatterns = [
path('',home,name='home'),
path('postdetails/<int:id>',postdetails,name='postdetails'),
# path('count_like/<int:id>',count_like,name='count_like'),
path('like_plus/<int:id>',like_plus,name='like_plus'),
path('like_minus/<int:id>',like_minus,name='like_minus'),

path('register/', register, name='register'),
path('login/', login, name='login'), 
path('logout/', logout, name='logout'), 

path('forget/', forget, name='forget'), 
path('c_password/', c_password, name='c_password'), 
path('trending',trending,name='trending'),
path('create_blog',create_blog,name='create_blog'),
path('search_fun',search_fun,name='search_fun'),
path('add_comment/<int:id>',add_comment,name='add_comment')


]




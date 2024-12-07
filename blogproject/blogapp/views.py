from django.shortcuts import render, redirect
from blogapp.models import *
from django.core.mail import send_mail
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if not User.objects.filter(username=username).exists() and not User.objects.filter(email=email).exists():
            User.objects.create(username=username, email=email, password=password)
            return redirect('login')  
        
    return render(request, 'login.html')

def create_blog(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        image = request.FILES.get("image")

        rid=User.objects.get(email=request.session['email'])
        blog.objects.create(
            User=rid,
            title=title,
            content=content,
            image=image,
        )

        messages.success(request, "Your blog has been successfully created!")
        return render(request,'createblog.html') 

    return render(request,'createblog.html') 

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = User.objects.filter(email=email).first()
        if not user:
            return render(request, 'login.html', {'error': 'Email does not exist.'})
        
        if user.password == password:
            request.session['email'] = email
            return redirect('home')  
        else:
            return render(request, 'login.html', {'error': 'Incorrect password.'})
    
    return render(request, 'login.html')
import random
def forget(request):
    if request.POST:
        email=request.POST['email']
        print(email)
        uid=User.objects.filter(email=email).exists()   
        otp=random.randint(1000,9999)
        print(otp)
        if uid:
            uid=User.objects.get(email=email)
            uid.otp=otp
            uid.save()
            send_mail('Forget password  :',f'OTP :{otp}','jitendradoriya92@gmail.com',[email])
            contaxt={
                'uid':uid
            }
            return render(request,'c_password.html',contaxt)
            
        else:
            contaxt={
                'msg':'Not Register yet '
            }
            return render(request,'forget.html',contaxt)
            
    return render(request,'forget.html')

def c_password(request):
    if request.POST:
        email=request.POST['email']
        otp=request.POST['otp']
        new_pass=request.POST['new_pass']
        con_pass=request.POST['con_pass']
        print(email,otp,new_pass,con_pass)
        uid=User.objects.get(email=email)
        print(type(uid.otp),type(otp))
        if uid.otp==int(otp):
            if new_pass == con_pass:
                uid.password = new_pass
                uid.save()
                return redirect(login)
            else:
                contaxt={
                    "msg":"invalid Password and C_Password",
                    "uid":uid
                    
                }
                return render(request,'c_password.html',contaxt)
        else:
            contaxt={
                    "msg":"invalid Otp",
                    "uid":uid
                }
            return render(request,'c_password.html',contaxt) 
                    
    return render(request,'c_password.html')


def home(request):
    if 'email' not in request.session:
        return redirect('login')  
    data = blog.objects.all()
    
    contaxt = {
        'data': data,
    }
    return render(request, 'home.html', contaxt)


def like_plus(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to like or dislike a post.")
        return redirect('login')  # Redirect to the login page if the user isn't authenticated

    # Fetch the blog post by ID manually
    blog_post = blog.objects.get(id=id)
    
    # Get the currently logged-in user
    rid = User.objects.get(email=request.session['email'])

    # Check if the user has already liked or disliked the post
    user_reaction = likes.objects.filter(blog=blog_post, User=rid).first()

    if user_reaction:
        if user_reaction.reaction_type == 'like':
            # If the user already liked, remove the like
            user_reaction.delete()
            if blog_post.l_add > 0:  # Ensure l_add does not go below 0
                blog_post.l_add -= 1
        else:
            # Prevent the user from switching directly from dislike to like
            messages.error(request, "You cannot like a post you have already disliked. Remove the dislike first.")
            return redirect('home')
    else:
        # Create a new like reaction with the current timestamp
        likes.objects.create(blog=blog_post, User=rid, reaction_type='like')
        
        blog_post.l_add += 1

    blog_post.save()
    return redirect(home)  # Redirect to the home page after reacting



def like_minus(request, id):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to like or dislike a post.")
        return redirect('login')

    # Fetch the blog post by ID manually
    blog_post = blog.objects.get(id=id)

    rid = User.objects.get(email=request.session['email'])
    
    user_reaction = likes.objects.filter(blog=blog_post, User=rid).first()

    if user_reaction:
        if user_reaction.reaction_type == 'dislike':
            # If the user already disliked, remove the dislike
            user_reaction.delete()
            if blog_post.l_add > 0:  # Ensure l_add does not go below 0
                blog_post.l_add -= 1
        else:
            # Prevent the user from switching directly from like to dislike
            messages.error(request, "You cannot dislike a post you have already liked. Remove the like first.")
            return redirect('home')
    else:
        likes.objects.create(blog=blog_post, User=rid, reaction_type='dislike')
        blog_post.dl_add += 1

    blog_post.save()
    return redirect(home)


def postdetails(request, id):
    if 'email' not in request.session:
        return redirect('login')
    
    data = blog.objects.get(id=id)
    rid=User.objects.get(email=request.session['email'])
    
    comm=comment.objects.filter(blog=data)
    
    contaxt = {
        'data': data,
        'comm':comm
    }
    return render(request, 'postdetails.html', contaxt)

def trending(request):
    if 'email' not in request.session:
        return redirect('login')
    
    data = trending_topics.objects.all()
    contaxt = {
        'data': data
    }
    return render(request, 'trending.html', contaxt)

def logout(request):
    del request.session['email']
    return redirect(home)


def search_fun(request):
    if request.POST:
        search=request.POST['search']
        # print(search,'hello')
        data=blog.objects.filter(title__contains=search)
        contaxt={
            'data':data
        }
        return render(request, 'home.html',contaxt)
    return redirect(home)

def add_comment(request,id):
    if request.POST:
        b=blog.objects.get(id=id)
        rid=User.objects.get(email=request.session['email'])
        
        message=request.POST['comment']
        comment.objects.create(User=rid,blog=b,message=message)
        return redirect(home)
    return render(request,'postdetails.html')
        
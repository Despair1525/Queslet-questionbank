from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

# from django.contrib.auth.forms import 
# Create your views here.

def login_users(request):

    if request.method =="POST":
        username = request.POST["username"]
        password = request.POST["password"]

        print(username)
        print(password)

        user = authenticate(request,username=username,password = password)

        if user is not None:
            login(request,user)
            #rediracnt to main page
            return redirect('home')
        else:

            
            #return an "invalid login"
            messages.success(request,("User or password not valid"))
            return redirect('login')

        
        pass
    else:

        return render(request,"authentication/login.html",{})

def logout_user(request):
    logout(request)
    messages.success(request,("You Were Logout"))
    return redirect('login')


def register_users(request):
    
    if request.method =="POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            print("Register User succesfully !")
            #add to default/ teachee group 
            teacher = Group.objects.get(name='teacher')
            user.groups.add(teacher)
            

            # login(request,user)
            return redirect('manage')
    else:
        form = UserCreationForm()


    return render(request,"authentication/register.html",{"form":form})
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from email_validator import validate_email


# Create your views here.
def loginuser(request):
    email=""
    if request.method=="POST":
        usernamedata=request.POST.get("username")
        password=request.POST.get("password")
        if not usernamedata:
              messages.info(request, " Enter a  email or username")
              return redirect("login")
        if not password:
              messages.info(request, "Enter a password")
              return redirect("login")

        try:
            validate_email(usernamedata)
            email=usernamedata
         
        except Exception as e:
            print(e)  
        if email:
                userqueryset=User.objects.filter(email=usernamedata)
                print(userqueryset)
                if userqueryset.exists():
                 username=userqueryset.first().email
                else:
                    messages.info(request, "Email or password is invalid")
                    return redirect("login")
        else:
                username=usernamedata
        
     
        if User.objects.filter(username=username).exists():
            user=authenticate(username=username,password=password)
            if user is None:
                  messages.info(request, "Username or password is invalid")
                  return redirect("login")
            else:
                login(request,user)
                return redirect("home")
        else:
            messages.info(request, "Username or password is invalid")
            return redirect("login")
    return render(request,"login.html")
def home(request):
    return render(request,"home.html")
def register(request):
    if request.method=="POST":
        email=request.POST.get("email")
        password=request.POST.get("password")
        username=request.POST.get("username")
        if not username:
            messages.info(request,"Plesae enter username")
            return redirect("register")
        if not password:
            messages.info(request,"Plesae enter password")
            return redirect("register")
        if not email:
            messages.info(request,"Plesae enter email")
            return redirect("register")
        
        if User.objects.filter(email=email ):
          messages.info(request, "The emial  is already in use.")
          return redirect("register")
        if User.objects.filter(username=username):
            messages.info(request, "The username  is already in use.")
            return redirect("register")
        user=User.objects.create(username=username,email=email)
        user.set_password(password)
        user.save()
        return redirect("login")

    return render(request,"register.html")
def logoutuser(request):
    logout(request)
    return render(request,"home.html")
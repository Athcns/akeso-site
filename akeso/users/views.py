from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User as Account

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request, "journal/library.html")
    return render(request, "users/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid Credentials"
            })
    else:
        return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return render(request, "users/index.html", {
        "message": "Logged Out"
    })

def register(request):
    if request.method == "POST":
        first_name = request.POST['name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm-password']
        if len(first_name) > 0:
            if not Account.objects.filter(username=username).exists():
                if not Account.objects.filter(email=email).exists():
                    if password == confirm_password:
                        user = Account.objects.create_user(first_name=first_name, username=username, email=email, password=password)
                        return render(request, "users/login.html", {
                            "message": "Account Created."
                        })
                    else:
                        error_message = "Passwords do not match"
                else:
                    error_message = "This email is already in use"
            else:
                error_message = "This username already exists"
        else:
            error_message = "First Name must be filled"

        return render(request, "users/register.html", {
            "message": error_message,
            "first_name": first_name,
            "username": username,
            "email": email,
        })


    return render(request, "users/register.html")
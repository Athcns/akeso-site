from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.models import User as Account
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags

import random, string
from .models import UserToken


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
                        if len(password) >= 5:
                            user = Account.objects.create_user(first_name=first_name, username=username, email=email, password=password)
                            return render(request, "users/login.html", {
                                "message": "Account Created."
                            })
                        else:
                            error_message = "Password must be 5 characters or longer"
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

def request_change(request):
    if request.method == "POST":
        enteredEmail = request.POST['email']
        try:
            validAccount = Account.objects.get(email=enteredEmail)

            # TODO: Create a way to make sure unique ID's arent repeated
            uniqueToken, created = UserToken.objects.get_or_create(user=validAccount)
            uniqueToken.token = ''.join(random.choice(string.ascii_uppercase + string.digits) for i in range(50))
            uniqueToken.save()

            subject = "Akeso Password Reset Requested"
            #email_template = "users/password_reset_email.html"
            email_template = "users/password_reset_email.txt"
            email_info = {
                "email": enteredEmail,
                "site_name": "Akeso",
                "userToken": uniqueToken.token,
                "protocol": "https",
                "domain": "akeso-journal.azurewebsites.net",
                "user": validAccount,
            }
            #html_email = render_to_string(email_template, email_info)
            #plain_email = strip_tags(html_email)

            plain_email = render_to_string(email_template, email_info)
            try:
                send_mail(subject, plain_email, "akesohelp@gmail.com", [enteredEmail], fail_silently=False)
            except BadHeaderError:
                return render(request, "users/request-email.html", {
                    "error_message": "Invalid Header Error"
                })

            return render(request, "users/request-email.html", {
                "valid_email": True
            })


        except Account.DoesNotExist:
            return render(request, "users/request-email.html", {
                "invalid_email": True
            })

    return render(request, "users/request-email.html")

# Changing password when the user forgot theirs
def change_unknown_pasword(request, token):
    user = Account.objects.get(usertoken__token = token)

    if request.method == "POST":
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        if newPassword == confirmPassword:
            if len(newPassword) >= 5:
                user.set_password(newPassword)
                user.save()

                return render(request, "users/login.html", {
                    "alert_success": "Password changed! Please log in again."
                })
            else:
                error_message = "Password must be 5 characters or longer"
        else:
            error_message = "Passwords are not matching"

        return render(request, "users/password-reset.html", {
            "user": user,
            "token": token,
            "alert_error": error_message
        })

    return render(request, "users/password-reset.html", {
        "user": user,
        "token": token
    })

# Changing password when the user is logged in
def change_password(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = Account.objects.get(id=request.user.id)
        if request.method == "POST":
            currentPassword = request.POST['currentPassword']
            newPassword = request.POST['newPassword']
            confirmPassword = request.POST['confirmPassword']

            validatePassword = authenticate(request, username = user.username, password = currentPassword)

            if validatePassword is not None:
                if newPassword == confirmPassword:
                    if len(newPassword) >= 5:
                        user.set_password(newPassword)
                        user.save()

                        logout(request)
                        return render(request, "users/index.html", {
                            "message": "Logged Out"
                        })
                    else:
                        error_message = "Password must be 5 characters or longer"
                else:
                    error_message = "Passwords are not matching"
            else:
                error_message = "Current Password wrong!"

            return render(request, "journal/settings.html", {
                "user": user,
                "error_message": error_message
            })
        return render(request, "journal/settings.html", {
            "user": user,
        })

def change_name(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = Account.objects.get(id=request.user.id)
        if request.method == "POST":
            newFirstName = request.POST['newFirstName']

            if len(newFirstName) >= 1:
                user.first_name = newFirstName
                user.save()

                return render(request, "journal/settings.html", {
                    "user": user
                })
            else:
                error_message = "First Name must be atleast 1 character"

            return render(request, "journal/settings.html", {
                "user": user,
                "error_message": error_message
            })

        return render(request, "journal/settings.html", {
            "user": user
        })
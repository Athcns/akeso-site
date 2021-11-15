from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse

from .models import Journal, Entry

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        library = Journal.objects.all()
        return render(request, "journal/journal.html", {
            "user_id": request.user.id,
            "journals": library
        })

def create(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            header = request.POST['header']
            content = request.POST['content']

            # Creates a new entry model and saves it
            new_entry = Entry(header=header, content=content)
            new_entry.save()

            return render(request, "journal/journal.html", {
                "user_id": request.user.id
            })
        library = Journal.objects.all()
        return render(request, "journal/create.html", {
        })

def read(request):
    pass
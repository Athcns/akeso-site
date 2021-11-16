from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse

from .models import Journal, Entry
from django.contrib.auth.models import User

#TODO: Create a way to view the entries details (Their Context and Header)

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        library = Journal.objects.filter(writer=user)

        # TODO: Allow users to see their Journals numbered 1, 2, 3,... rather than just the
        # primary key number auto assigned to the journal on creation.
        return render(request, "journal/library.html", {
            "journals": library
        })


def create_entry(request, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        journal = Journal.objects.get(id=journalID)

        if request.method == "POST":
            header = request.POST['header']
            content = request.POST['content']

            # Creates a new entry model and saves it
            newEntry = Entry(header=header, content=content)
            newEntry.save()
            newEntry.journal_id.add(journal)

            entries = Entry.objects.filter(journal_id=journalID)
            return render(request, "journal/journal.html", {
                "journal":journal,
                "entries":entries
            })

        return render(request, "journal/create.html", {
            "journal": journal
        })


def create_journal(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            name = request.POST['journalName']
            user = User.objects.get(id=request.user.id)

            newJournal = Journal(writer=user, name=name)
            newJournal.save()

            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))


def journal_view(request, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        journal = Journal.objects.get(id=journalID)
        entries = Entry.objects.filter(journal_id=journalID)

        return render(request, "journal/journal.html", {
            "journal": journal,
            "entries": entries
        })



def read(request, entry_id):
    pass

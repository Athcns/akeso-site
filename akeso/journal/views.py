from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse

from .models import Journal, Entry, Activity, Mood, Status, WeeklyUpdate
from django.contrib.auth.models import User
from datetime import datetime

#TODO: Create a way to view the entries details (Their Context and Header)
#TODO: Create a custom ID number creator for each model created (besides just counting from 1)

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        library = Journal.objects.filter(writer=user)
        moodStatus = Mood.objects.filter(user_id=user, creation_date=date)
        activities = Activity.objects.filter(user_id=user)
        # TODO: Allow users to see their Journals numbered 1, 2, 3,... rather than just the
        # primary key number auto assigned to the journal on creation.
        if moodStatus:
            return render(request, "journal/library.html", {
                "journals": library,
                "activities": activities,
                "daily_mood": False
            })
        else:
            return render(request, "journal/library.html", {
                "journals": library,
                "activities": activities,
                "daily_mood": True
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

def mood(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)

            mood = request.POST['mood_scale']
            activities = request.POST['activities']

            newMood = Mood(user_id=user, mood_scale=mood, activity=activities)
            newMood.save()

            return HttpResponseRedirect(reverse("index"))

def activity_view(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login" ))
    else:
        user = User.objects.get(id=request.user.id)
        activities = Activity.objects.filter(user_id=user)

        return render(request, "journal/activity.html", {
            "activities": activities,
        })

def create_activity(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)
            activity_name = request.POST['activity']

            newActivity = Activity(name=activity_name, user_id=user)
            newActivity.save()

            return HttpResponseRedirect(reverse("viewActivity"))
        return HttpResponseRedirect(reverse("viewActivity"))

def delete_activity(request, activityID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        # Grabs the correlating activity and deletes it
        activity = Activity.objects.get(id=activityID)
        activity_name = activity.name
        activity.delete()

        user = User.objects.get(id=request.user.id)
        activities = Activity.objects.filter(user_id=user)

        # Returns the user to original activity page with the message clarifying an activity has been deleted
        return render(request, "journal/activity.html", {
            "activities": activities,
            "message": f"{activity_name} has been deleted"
        })

def read(request, entryID,journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        entry = Entry.objects.get(id=entryID)
        journal = Journal.objects.get(id=journalID)
        return render(request, "journal/entry.html", {
            "entry": entry,
            "journal": journal
        })
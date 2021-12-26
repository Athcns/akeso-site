from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse

from .models import Journal, Entry, Activity, Mood, Status, WeeklyUpdate
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta

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

# Allows users to create mood reports for their day
# TODO: Allow people to recreate a mood report for the day (Eg. accidently submited)
# TODO: Compile all the moods in the week and give a weekly update/suggestions
def create_mood(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            user = User.objects.get(id=request.user.id)

            mood = request.POST['mood_scale']
            activities = request.POST.getlist('activity')

            newMood = Mood(user_id=user, mood_scale=mood)
            newMood.save()
            for name in activities:
                selectedActivity = Activity.objects.get(user_id=user, name=name)
                newMood.activity.add(selectedActivity)
                newMood.save()

            return HttpResponseRedirect(reverse("index"))

def delete_mood(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        date = str(datetime.today().year) + "-" + str(datetime.today().month) + "-" + str(datetime.today().day)
        moodReport = Mood.objects.get(user_id=user, creation_date=date)
        library = Journal.objects.filter(writer=user)
        activities = Activity.objects.filter(user_id=user)

        if moodReport:
            moodReport.delete()
            return HttpResponseRedirect(reverse("index"))

def create_weekly_update(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)

        currentDate = date.today()
        currentWeekday = currentDate.weekday()
        week = []
        for i in range(0 - currentWeekday, 7 - currentWeekday):
            week.append(currentDate + timedelta(days=i))

        weekMoods = Mood.objects.filter(user_id=user,
                                        creation_date__range=[week[0].strftime("20%y-%m-%d"),
                                                              week[6].strftime("20%y-%m-%d")])

        if weekMoods:
            # Create a weekly status report to connect to the status reports
            weeklyUpdate = WeeklyUpdate(user_id=user)
            weeklyUpdate.save()

            # Iterates through each mood made in that week
            for i in weekMoods:
                # Grabs the mood report's date and the specific day name (eg. Sunday)
                day = datetime.strptime(i.creation_date, "20%y-%m-%d").strftime("%A")

                # Creates a new Status report that will connect the mood report to the weekly update
                newStatus = Status(user_id=user,
                                   mood_id=i,
                                   activity=i.activity,
                                   week_date=i.creation_date,
                                   week_name=day)
                newStatus.save()

                # Connects the new Status to the weekly update created above
                weeklyUpdate.add(newStatus)

        else:
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
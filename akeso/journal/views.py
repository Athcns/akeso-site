from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate
from django.urls import reverse

from .models import Journal, Entry, Activity, Mood, Status, WeeklyUpdate
from django.contrib.auth.models import User
from datetime import datetime, date, timedelta
import json
from .common import currentWeek, weekdays

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        currentDate = str(date.today())
        library = Journal.objects.filter(writer=user).order_by("-creation_date")
        moodStatus = Mood.objects.filter(user_id=user, creation_date=currentDate)
        # Check if there is an existing Mood Status for the day
        moodValid = False
        if moodStatus:
            moodValid = True

        activities = Activity.objects.filter(user_id=user)

        return render(request, "journal/library.html", {
            "journals": library,
            "activities": activities,
            "daily_mood": moodValid,
        })

def settings(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)

        return render(request, "journal/settings.html", {
            "user": user
        })


def create_entry(request, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        journal = Journal.objects.get(id=journalID)

        if request.method == "POST":
            header = request.POST['header']
            content = request.POST['content']
            currentTime = datetime.now()

            # Creates a new entry model and saves it
            newEntry = Entry(header=header, content=content, journal_id=journal, accessed_date=currentTime)
            newEntry.save()

            entries = Entry.objects.filter(journal_id=journalID).order_by("-creation_date")
            return render(request, "journal/journal.html", {
                "journal":journal,
                "entries":entries
            })

        return render(request, "journal/create.html", {
            "journal": journal
        })

def view_entry(request, entryID, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        try:
            journal = Journal.objects.get(id=journalID, writer=user)
            entry = Entry.objects.get(id=entryID, journal_id__writer=user, journal_id=journal)

            # Updating the accessed date/time once the entry opens
            entry.accessed_date = datetime.now()
            entry.save()
            journal.accessed_date = datetime.now()
            journal.save()

            return render(request, "journal/entry.html", {
                "entry": entry,
                "journal": journal
            })
        except Journal.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))
        except Entry.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

def delete_entry(request, entryID, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        try:
            # Prevents users from deleting other documents or other people's entries
            entry = Entry.objects.get(id=entryID, journal_id=journalID, journal_id__writer=user)
            entry.delete()

            entries = Entry.objects.filter(journal_id=journalID).order_by("-creation_date")
            journal = Journal.objects.get(id=journalID)

            return render(request, "journal/journal.html", {
                "journal": journal,
                "entries": entries
            })
        except Entry.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

def create_journal(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        if request.method == "POST":
            name = request.POST['journalName']
            user = User.objects.get(id=request.user.id)
            currentTime = datetime.now()

            newJournal = Journal(writer=user, name=name, accessed_date=currentTime)
            newJournal.save()

            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse("index"))


def view_journal(request, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        # Prevents other uses from accessing the journals
        try:
            journal = Journal.objects.get(id=journalID, writer=user)
            entries = Entry.objects.filter(journal_id=journalID).order_by("-creation_date")

            journal.accessed_date = datetime.now()
            journal.save()

            return render(request, "journal/journal.html", {
                "journal": journal,
                "entries": entries
            })
        except Journal.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

def delete_journal(request, journalID):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        try:
            # Prevents users from deleting other documents or other people's entries
            journal = Journal.objects.get(id=journalID, writer=user)
            journal.delete()

            return HttpResponseRedirect(reverse("index"))
        except Journal.DoesNotExist:
            return HttpResponseRedirect(reverse("index"))

# Allows users to create mood reports for their day
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
        currentDate = str(date.today())
        moodReport = Mood.objects.get(user_id=user, creation_date=currentDate)
        library = Journal.objects.filter(writer=user)
        activities = Activity.objects.filter(user_id=user)

        if moodReport:
            moodReport.delete()
            return HttpResponseRedirect(reverse("index"))

def view_weekly_update(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        allWeeklyReports = WeeklyUpdate.objects.filter(user_id=user).order_by("-creation_date")

        if request.method == "POST":
            # Grabs the weekly report from the desired week
            weeklyReportID = request.POST['week']
            weeklyReport = WeeklyUpdate.objects.get(id=weeklyReportID)
            weeklyValid = True

            # Grabs the dates for the desired week and checks whether the week is the current one or not
            week = weekdays(weeklyReport.start_week)
            currentBool = False
            if week == currentWeek():
                currentBool = True
            # Filters through the Mood objects to find everything in range of the dates
            weeklyMood = Mood.objects.filter(user_id=user,
                                             creation_date__range=[week[0].strftime("%Y-%m-%d"),
                                                                   week[6].strftime("%Y-%m-%d")])

            weekDates = []
            moodScales = []
            # Iterates through each day in the week and trys to assign a coresponding mood scale for that day
            for date in week:
                weekDates.append(date.strftime("%a (%d-%m-%Y)"))
                try:
                    moodReport = weeklyMood.get(user_id=user,
                                                creation_date=date.strftime("%Y-%m-%d"))
                    moodScales.append(moodReport.mood_scale)
                except Mood.DoesNotExist:
                    moodScales.append(None)

            monday = week[0].strftime('%d-%m-%Y')
            sunday = week[6].strftime('%d-%m-%Y')
            title = f"Weekly Report ({monday} - {sunday})"

            return render(request, "journal/weekly-report.html", {
                "weekly_report": weeklyValid,
                "currentWeek": currentBool,
                "best_day": weeklyReport.best_day,
                "average_value": weeklyReport.average_value,
                "num_of_reports": weeklyReport.num_of_moods,
                "often_activity": weeklyReport.often_activity,
                "often_value": weeklyReport.often_value,
                "suggested_activity": weeklyReport.suggested_activity,
                "weeks": allWeeklyReports,
                "labels": weekDates,
                "data": json.dumps(moodScales),
                "graph_title": title
            })

        else:
            # Grabs the dates for the current week (Monday to Sunday)
            week = currentWeek()
            # Filters through the weeklyUpdate model and weeklyMood
            weeklyMood = Mood.objects.filter(user_id=user,
                                                       creation_date__range=[week[0].strftime("%Y-%m-%d"),
                                                                             week[6].strftime("%Y-%m-%d")])
            weeklyReport = WeeklyUpdate.objects.filter(user_id=user,
                                             creation_date__range=[week[0].strftime("%Y-%m-%d"),
                                                                   week[6].strftime("%Y-%m-%d")])
            # Checks if there is an existing weeklyReport created for the current week
            weeklyValid = False
            if weeklyReport:
                weeklyValid = True

                weekDates = []
                moodScales = []
                # Iterates through each day in the week and trys to assign a coresponding mood scale for that day
                for date in week:
                    weekDates.append(date.strftime("%a (%d-%m-%Y)"))
                    try:
                        moodReport = weeklyMood.get(user_id=user,
                                                        creation_date=date.strftime("%Y-%m-%d"))
                        moodScales.append(moodReport.mood_scale)
                    except Mood.DoesNotExist:
                        moodScales.append(None)

            if weeklyValid:
                # Grabs the dates to make the title of the graph
                monday = week[0].strftime('%d-%m-%Y')
                sunday = week[6].strftime('%d-%m-%Y')
                title = f"Weekly Report ({monday} - {sunday})"

                return render(request, "journal/weekly-report.html", {
                    "weekly_report": weeklyValid,
                    "currentWeek": True,
                    "best_days": Status.objects.filter(best_day__id=weeklyReport[0].id),
                    "average_value": weeklyReport[0].average_value,
                    "num_of_reports": weeklyReport[0].num_of_moods,
                    "often_activity": weeklyReport[0].often_activity,
                    "often_value": weeklyReport[0].often_value,
                    "suggested_activities": Activity.objects.filter(weeklyupdate__id=weeklyReport[0].id),
                    "weeks": allWeeklyReports,
                    "labels": weekDates,
                    "data": json.dumps(moodScales),
                    "graph_title": title
                })
            else:
                return render(request, "journal/weekly-report.html", {
                    "weekly_report": weeklyValid,
                    "currentWeek": True,
                    "weeks": allWeeklyReports
                })

def create_weekly_update(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)

        # Grabs the dates for the current week through the common.py function
        week = currentWeek()

        weekMoods = Mood.objects.filter(user_id=user,
                                        creation_date__range=[week[0].strftime("20%y-%m-%d"),
                                                              week[6].strftime("20%y-%m-%d")])

        # Checks if the user has made any mood reports for that week
        if weekMoods:
            # Create a weekly status report to connect to the status reports
            weeklyUpdate = WeeklyUpdate(user_id=user)

            weeklyUpdate.save()

            # Iterates through each mood made in that week
            for i in weekMoods:
                # Grabs the mood report's date and the specific day name (eg. Sunday)
                day = datetime.strptime(str(i.creation_date), "20%y-%m-%d").strftime("%A")

                # Creates a new Status report that will connect the mood report to the weekly update
                newStatus = Status(user_id=user,
                                   mood_id=i,
                                   week_date=i.creation_date,
                                   day_name=day)
                newStatus.save()
                newStatus.activity.set(i.activity.all())
                newStatus.save()

                # Connects the new Status to the weekly update created above
                weeklyUpdate.status_id.add(newStatus)

            # Creating Stats for the weeklyUpdate
            # Makes a queryset of the Moods for that week ordered by their mood scale (descending)
            ordered_status = weekMoods.order_by('-mood_scale')
            bestDayStatus = Status.objects.get(user_id=user, mood_id=ordered_status[0])
            weeklyUpdate.best_day.add(bestDayStatus)
            weeklyUpdate.start_week = week[0].strftime("20%y-%m-%d")
            weeklyUpdate.end_week = week[6].strftime("20%y-%m-%d")
            temp_mood = 0
            for i in ordered_status:
                temp_mood += i.mood_scale
            weeklyUpdate.average_value = ((temp_mood/len(ordered_status)))
            weeklyUpdate.num_of_moods = (len(ordered_status))

            oft_activities = {}
            sug_activities = {}
            order_activities = []
            # Iterates through each Mood in the query set
            for i in ordered_status:
                # Iterates through each activity inside a specific Mood
                for j in i.activity.all():
                    if j.name in oft_activities:
                        oft_activities[j.name] += 1
                        #                        adds 1 to the number of occurrences this activity appeared this week
                        sug_activities[j.name][0] += 1
                        #                        adds the mood scale for that day to the sum of mood scale
                        sug_activities[j.name][1] += i.mood_scale
                    else:
                        oft_activities[j.name] = 1
                        #                        [num of occurrences, sum of mood scale, mean of the mood scale]
                        sug_activities[j.name] = [1, i.mood_scale, None]
                        order_activities.append(j.name)

            weeklyUpdate.often_activity = (Activity.objects.get(name=max(oft_activities), user_id=user))
            weeklyUpdate.often_value = (oft_activities[max(oft_activities)])
            weeklyUpdate.save()

            # Iterates through the suggested activities dictionary to find the mean values of each
            for key, value in sug_activities.items():
                # Calculates the mean mood scale by dividing the Sum of Mood Scale by the Num of Occurrences
                meanMood = (value[1]/value[0])
                # Places the calculated mean value into the dictionary
                sug_activities[key][2] = meanMood

            # Bubble sort the activities based on the mean mood scale for each (descending)
            for i in range(len(order_activities)):
                for j in range(len(order_activities) - i - 1):
                    if sug_activities[order_activities[j]][2] < sug_activities[order_activities[j + 1]][2]:
                        order_activities[j], order_activities[j + 1] = order_activities[j + 1], order_activities[j]

            # Adds all the suggested activities to the weeklyUpdate object
            switch = True
            while switch:
                for i in range(len(order_activities)):
                    if sug_activities[order_activities[i]][2] == sug_activities[order_activities[0]][2]:
                        suggestedActivity = Activity.objects.get(user_id=user, name=order_activities[i])
                        weeklyUpdate.suggested_activity.add(suggestedActivity)
                    else:
                        switch = False

            weeklyUpdate.save()

            return HttpResponseRedirect(reverse("viewWeeklyReport"))

        else:
            return HttpResponseRedirect(reverse("viewWeeklyReport"))

def delete_weekly_update(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        user = User.objects.get(id=request.user.id)
        currentDate = date.today()
        week = currentWeek()

        # Grabs all the status created in the corresponding week
        weekStatus = Status.objects.filter(user_id=user,
                                            creation_date__range=[week[0].strftime("%Y-%m-%d"),
                                                                    week[6].strftime("%Y-%m-%d")])
        # Grabs the weeklyUpdate object made in the corresponding week
        weekReport = WeeklyUpdate.objects.get(user_id=user,
                                              creation_date__range=[week[0].strftime("%Y-%m-%d"),
                                                                    week[6].strftime("%Y-%m-%d")])
        # Deletes the Status and WeeklyUpdate objects created
        weekReport.delete()
        weekStatus.delete()

        return HttpResponseRedirect(reverse("viewWeeklyReport"))

def view_activity(request):
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
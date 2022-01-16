from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("settings", views.settings, name="settings"),
    path("create-mood", views.create_mood, name="mood"),
    path("delete-mood", views.delete_mood, name="deleteMood"),
    path("activities", views.view_activity, name="viewActivity"),
    path("create-activity", views.create_activity, name="createActivity"),
    path("delete-activity/<int:activityID>", views.delete_activity, name="deleteActivity"),
    path("weekly-report", views.view_weekly_update, name="viewWeeklyReport"),
    path("create-weekly-report", views.create_weekly_update, name="createWeeklyReport"),
    path("delete-weekly-report", views.delete_weekly_update, name="deleteWeeklyReport"),
    path("<int:journalID>/create", views.create_entry, name="createEntry"),
    path("<int:journalID>/entry/<int:entryID>", views.view_entry, name="readEntry"),
    path("<int:journalID>/entry-delete/<int:entryID>", views.delete_entry, name="deleteEntry"),
    path("create-journal", views.create_journal, name="createJournal"),
    path("<int:journalID>", views.view_journal, name="viewJournal"),
    path("delete-journal/<int:journalID>", views.delete_journal, name="deleteJournal")
]
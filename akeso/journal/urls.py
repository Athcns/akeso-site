from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("", views.mood, name="mood"),
    path("activities", views.activity_view, name="viewActivity"),
    path("create-activity", views.create_activity, name="createActivity"),
    path("delete-activity/<int:activityID>", views.delete_activity, name="deleteActivity"),
    path("<int:journalID>/create", views.create_entry, name="createEntry"),
    path("<int:journalID>/entry/<int:entryID>", views.read, name="readEntry"),
    path("create-journal", views.create_journal, name="createJournal"),
    path("<int:journalID>", views.journal_view, name="viewJournal")
]
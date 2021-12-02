from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:journalID>/create", views.create_entry, name="createEntry"),
    path("<int:journalID>/entry/<int:entryID>", views.read, name="readEntry"),
    path("create-journal", views.create_journal, name="createJournal"),
    path("<int:journalID>", views.journal_view, name="viewJournal")
]
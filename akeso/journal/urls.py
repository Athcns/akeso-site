from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("read", views.read, name="read"),
    path("create-journal", views.create_journal, name="createJournal")
]
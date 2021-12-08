from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Journal(models.Model):
    # Assigns each account user's primary key to a journal table
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.id}"

class Entry(models.Model):
    # Accesses the entries with the same journal primary keys
    journal_id = models.ManyToManyField(Journal)
    # Creation date is set using datetime.datetime in views.py
    creation_date = models.DateTimeField(auto_now_add=True)
    # Auto sets date for when the model is opened
    accessed_date = models.DateTimeField(auto_now=True)
    # Header for the journal | max 100 chars
    header = models.CharField(max_length=100)
    # Entry Details
    content = models.TextField()

    def __str__(self):
        return f"{self.header}"

class Activity(models.Model):
    # Connects the activity to the specific user
    user_id = models.ForeignKey(User)
    # Activity name (Eg. Mediation)
    activity_name = models.CharField(max_length=64)
    # Date of Creation
    creation_date = models.DateTimeField(auto_now_add=True)

class Mood(models.Model):
    # Connects the mood to the user
    user_id = models.ForeignKey(User)
    # Connects the mood to the Entry
    entry_id = models.ManyToManyField(Entry)
    # Creates a scale from 1 to 10
    mood_scale = models.IntegerField(max_value=10, min_value=0)
    # Done activities
    activity = models.ForeignKey(Activity)
    # Created date
    creation_date = models.DateTimeField(auto_now_add=True)

class WeeklyUpdate(models.Model):
    user_id = models.ForeignKey(User)
    mood_id = models.ForeignKey(Mood)
    status_id = models.ForeignKey(Status)

class Status(models.Model):
    # Connect to user model
    user_id = models.ForeignKey(User)


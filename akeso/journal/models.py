from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Journal(models.Model):
    # Assigns each account user's primary key to a journal table
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    accessed_date = models.DateTimeField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.writer} | {self.id}"

class Entry(models.Model):
    # Accesses the entries with the same journal primary keys
    journal_id = models.ForeignKey(Journal, on_delete=models.CASCADE)
    # Creation date is set using datetime.datetime in views.py
    creation_date = models.DateTimeField(auto_now_add=True)
    # Auto sets date for when the model is opened
    accessed_date = models.DateTimeField()
    # Header for the journal | max 100 chars
    header = models.CharField(max_length=100)
    # Entry Details
    content = models.TextField()

    def __str__(self):
        return f"{self.header}"

class Activity(models.Model):
    # Connects the activity to the specific user
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # Activity name (Eg. Mediation)
    name = models.CharField(max_length=64)
    # Date of Creation
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}"

class Mood(models.Model):
    #TODO: When creating the function in views.py, make sure to add a check if the mood scale POSTed is between 1 and 10

    # Connects the mood to the user
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # Connects the mood to the Entry
    # entry_id = models.ManyToManyField(Entry)
    # Creates a scale from 1 to 10
    mood_scale = models.IntegerField(default=5)
    # Done activities
    activity = models.ManyToManyField(Activity)
    # Created date
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.creation_date}"

class Status(models.Model):
    # Connect to user model
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    # Mood from that day
    mood_id = models.ForeignKey(Mood, on_delete=models.CASCADE)
    # Activities from that day
    activity = models.ManyToManyField(Activity)
    # Weekday Date For the specified mood
    week_date = models.DateField(auto_now_add=False)
    # Weekday name and date (Eg. "Sunday, Dec 26, 2021)
    day_name = models.CharField(max_length=50)
    # Creation date and time
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id} - {self.creation_date}"

class WeeklyUpdate(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_week = models.DateField(null=True)
    end_week = models.DateField(null=True)

    # Links to the status models created for that week
    status_id = models.ManyToManyField(Status, related_name="status_id")
    creation_date = models.DateField(auto_now_add=True)

    # The highest mood scale day(s) of that week
    best_day = models.ManyToManyField(Status, related_name="best_day")

    # Mean value of the mood that week
    average_value = models.IntegerField(null=True)
    # Days in the week where the mood has been made
    num_of_moods = models.IntegerField(null=True)

    # Stats for the most often occuring activity in that week
    often_activity = models.ForeignKey(Activity, on_delete=models.CASCADE, null=True)
    often_value = models.IntegerField(null=True)

    # Activity that is suggested to improve mood
    suggested_activity = models.ManyToManyField(Activity, related_name="suggested_activity")

    def __str__(self):
        return f"{self.user_id} | {self.id} | {self.creation_date}"


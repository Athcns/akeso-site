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
    # TODO: Add a connection between the journal_id and each user's journals
    #journal_id = models.ManyToManyField(Journal, on_delete=models.CASCADE, related_name="book")
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
from django.db import models

# Create your models here.
class Journal(models.Model):
    # Assigns each account user's primary key to a journal table
    writer = models.ForeignKey( PLACEHOLDER )

    def __str__(self):
        return f"{self.id}"

class Entry(models.Model):
    # Accesses the entries with the same journal primary keys
    journal_id = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name="book")
    # Creation date is set using datetime.datetime in views.py
    creation_date = models.DateTimeField
    # Auto sets date for when the model is opened
    accessed_date = models.DateTimeField(auto_now=True)
    # Header for the journal | max 100 chars
    header = models.CharField(max_length=100)
    # Entry Details
    details = models.CharField

from django.contrib import admin

from .models import Journal, Entry, Activity, Mood, Status, WeeklyUpdate

# Register your models here.
# Journal related
admin.site.register(Journal)
admin.site.register(Entry)

# Mood related
admin.site.register(Activity)
admin.site.register(Mood)
admin.site.register(Status)
admin.site.register(WeeklyUpdate)
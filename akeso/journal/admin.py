from django.contrib import admin

from .models import Journal, Entry, Activity, Mood, Status, WeeklyUpdate

# Register your models here.
admin.site.register(Journal)
admin.site.register(Entry)
admin.site.register(Activity)
admin.site.register(Mood)
admin.site.register(Status)
admin.site.register(WeeklyUpdate)
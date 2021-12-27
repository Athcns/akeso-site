# Common Functions used in the views.py within the Journal App
from datetime import datetime, date, timedelta

def currentWeek():
    currentDate = date.today()
    currentWeekday = currentDate.weekday()
    week = []
    for i in range(0 - currentWeekday, 7 - currentWeekday):
        week.append(currentDate + timedelta(days=i))

    return week


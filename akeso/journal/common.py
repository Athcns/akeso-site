# Common Functions used in the views.py within the Journal App
from datetime import datetime, date, timedelta

def currentWeek():
    currentDate = date.today()
    currentWeekday = currentDate.weekday()
    week = []
    for i in range(0 - currentWeekday, 7 - currentWeekday):
        week.append(currentDate + timedelta(days=i))

    return week

def weekdays(selectedDate):
    # It will be the first day in a week
    startDay = selectedDate
    # Therefore the startweekDay is 0 being Monday, 6 being Sunday
    startWeekday = 0
    week = []
    for i in range(7):
        week.append(startDay + timedelta(days=i))

    return week

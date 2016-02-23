__author__ = 'Neil Butcher'

from datetime import time, date, datetime


StandardEventTimes = []
StandardEventTimes.append(('noon', time(12, 00, 00)))
StandardEventTimes.append(('midnight', time(00, 00, 00)))


def time_string(a_time):
    for seTime in StandardEventTimes:
        if a_time == seTime[1]:
            return seTime[0]
    return a_time.strftime("%H:%M")


def date_string(a_date):
    return a_date.strftime("%d. %B %Y")

def get_time(a_string):
    for seTime in StandardEventTimes:
        if a_string == seTime[0]:
            return seTime[1]
    return (time.strptime(a_string, "%H:%M")).time()


def get_date(a_string):
    return (datetime.strptime(a_string, "%d. %B %Y")).date()
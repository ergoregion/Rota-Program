__author__ = 'Neil Butcher'

from Rota_System.Reporting.HTMLObjects import HTMLObjects
from Rota_System.StandardTimes import date_string, time_string


def date(an_object):
    return an_object.date


def time(an_object):
    return an_object.time


def role(an_object):
    return an_object.role



def event_title(event):
        title = ''
        title += date_string(event.date)
        title += '   '
        title += time_string(event.time)
        title += '   '
        title += event.title
        return title

class AbstractMultiAppointmentReporter(object):
    def events(self, events):
        self._events = events
        self._all_appointments = set()

    def html(self):
        html = HTMLObjects.HTMLGroup()
        html.add(self._html_preheader())
        html.add(self._html_header())
        if len(self._all_appointments) > 0:
            html.add(self._html_table())
        html.add(self._html_footer())
        return html

    def _html_preheader(self):
        return None

    def _html_header(self):
        return None

    def _html_table(self):
        return None

    def _html_footer(self):
        return None

    def _dates(self):
        return sorted(set(map(date, self._events)))

    def _times(self):
        return sorted(set(map(time, self._all_appointments)))

__author__ = 'Neil Butcher'

from HTMLObjects import HTMLObjects


def date(an_object):
    return an_object.date


def time(an_object):
    return an_object.time


def role(an_object):
    return an_object.role


def person_name(an_object):
    if an_object.isFilled():
        return an_object.person.name
    else:
        return 'Not filled'


class AbstractMultiAppointmentReporter(object):
    def events(self, events):
        self._events = events
        self._all_appointments = set()

    def html(self):
        if len(self._all_appointments) == 0:
            return HTMLObjects.HTMLNone()
        html = HTMLObjects.HTMLGroup()
        html.add(self._html_header())
        html.add(self._html_table())
        html.add(self._html_footer())
        return html

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

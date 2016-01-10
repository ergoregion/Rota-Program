__author__ = 'Neil Butcher'

from HTMLObjects import HTMLObjects
from Abstract import AbstractMultiAppointmentReporter, person_name
from Rota_System.StandardTimes import time_string, date_string


class RoleReporter(AbstractMultiAppointmentReporter):
    '''
    produces a html from a role and a list of events
    '''

    def report_about(self, an_object):
        if not self._events:
            return HTMLObjects.HTMLNone()
        self.role(an_object)
        return self.html().html_string()

    def role(self, role):

        self._all_appointments = set()
        self._role = role
        for e in self._events:
            correct_appointments = filter(lambda x: x.role == role, e.appointments)
            self._all_appointments.update(correct_appointments)

    def _html_header(self):
        return HTMLObjects.HTMLTitle(self._role.description)

    def _html_table(self):
        table = HTMLObjects.HTMLTable()
        row = HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableHeaderCell())
        for t in self._times():
            row.add(HTMLObjects.HTMLTableHeaderCell(time_string(t)))
        table.add(row)
        for d in self._dates():
            row = HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableHeaderCell(date_string(d)))
            for t in self._times():
                correct_appointments = filter(lambda x: x.date == d and x.time == t, self._all_appointments)
                names = map(person_name, correct_appointments)
                if len(names) > 0:
                    string = '<br>'.join(names)
                else:
                    string = ''
                row.add(HTMLObjects.HTMLTableCell(string))
            table.add(row)
        return table

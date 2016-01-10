__author__ = 'Neil Butcher'

from HTMLObjects import HTMLObjects
from datetime import datetime
from Rota_System.StandardTimes import date_string, time_string
from Abstract import AbstractMultiAppointmentReporter


class PersonReporter(AbstractMultiAppointmentReporter):
    '''
    produces a html from a person and a list of events
    '''

    def report_about(self, an_object):
        if not self._events:
            return HTMLObjects.HTMLNone()
        self.person(an_object)
        return self.html().html_string()

    def person(self, person):

        self._all_appointments = set()
        self._person = person
        for e in self._events:
            correct_appointments = filter(lambda x: x.person == person, e.appointments)
            self._all_appointments.update(correct_appointments)
        self._sorted_appointments = sorted(self._all_appointments, key=lambda app: datetime.combine(app.date, app.time))

    def _html_header(self):
        return HTMLObjects.HTMLTitle(self._person.name)

    def _html_table(self):
        table = HTMLObjects.HTMLTable(self._html_table_header_row())
        for appointment in self._sorted_appointments:
            row = self._html_table_row_for_appointment(appointment)
            table.add(row)
        return table

    def _html_table_row_for_appointment(self, appointment):
        html = HTMLObjects.HTMLTableRow()
        html.add(HTMLObjects.HTMLTableCell(date_string(appointment.date)))
        time = time_string(appointment.time)
        event = str(appointment.event.description)
        html.add(HTMLObjects.HTMLTableCell(time))
        html.add(HTMLObjects.HTMLTableCell(self._role_description(appointment)))
        html.add(HTMLObjects.HTMLTableCell(event))
        return html

    def _role_description(self, appointment):
        roleDescription = appointment.role.description
        if appointment.note is not None and len(appointment.note) > 0 and appointment.note is not 'None':
            roleDescription += '('
            roleDescription += appointment.note
            roleDescription += ')'
        return roleDescription

    def _html_table_header_row(self):
        html = HTMLObjects.HTMLTableRow()
        html.add(HTMLObjects.HTMLTableHeaderCell('Date'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Time'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Role'))
        html.add(HTMLObjects.HTMLTableHeaderCell('event'))
        return html

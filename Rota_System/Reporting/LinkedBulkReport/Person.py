__author__ = 'Neil Butcher'

from Rota_System.Reporting.HTMLObjects import HTMLObjects
from datetime import datetime
from Rota_System.StandardTimes import date_string, time_string
from Abstract import AbstractMultiAppointmentReporter, event_title, person_code


class PopulationReporter(object):
    def events(self, events):
        self._reporter = PersonReporter()
        self._reporter.events(events)

    def write_reports_about(self, a_list, a_folder):
        if not self._reporter.events:
            return HTMLObjects.HTMLNone()
        self._write_index_file(a_list, a_folder)
        for person in a_list:
            html = self._reporter.report_about(person)
            filename = a_folder + '\\' + person_code(person) + '.html'
            fileopen = open(filename, 'w')
            fileopen.write(html.html_string())
            fileopen.close()

    def _write_index_file(self, a_list, a_folder):

        table = HTMLObjects.HTMLTable()
        for person in a_list:
            text = HTMLObjects.HTMLLink(person_code(person), "./" + person_code(person) + ".html")
            cell = HTMLObjects.HTMLTableCell(text)
            row = HTMLObjects.HTMLTableRow(cell)
            table.add(row)

        html = HTMLObjects.HTMLAll(HTMLObjects.HTMLHead(HTMLObjects.HTMLPageTitle('People')))
        html.add(HTMLObjects.HTMLLink("index", "../index.html"))
        html.add(HTMLObjects.HTMLTitle('People'))
        html.add(table)
        filename = a_folder + '\\' + 'index.html'
        fileopen = open(filename, 'w')
        fileopen.write(html.html_string())
        fileopen.close()


class PersonReporter(AbstractMultiAppointmentReporter):
    '''
    produces a html from a person and a list of events
    '''

    def report_about(self, an_object):
        if not self._events:
            return HTMLObjects.HTMLNone()
        self.person(an_object)
        return self.html()

    def person(self, person):

        self._all_appointments = set()
        self._person = person
        for e in self._events:
            correct_appointments = filter(lambda x: x.person == person, e.appointments)
            self._all_appointments.update(correct_appointments)
        self._sorted_appointments = sorted(self._all_appointments, key=lambda app: datetime.combine(app.date, app.time))

    def _html_preheader(self):
        return HTMLObjects.HTMLLink("people", "./index.html")

    def _html_header(self):
        return HTMLObjects.HTMLTitle(person_code(self._person))

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
        event_link = HTMLObjects.HTMLLink(appointment.event.title, "../events/" + event_title(appointment.event) + ".html")
        html.add(HTMLObjects.HTMLTableCell(time))
        html.add(HTMLObjects.HTMLTableCell(self._role_description(appointment)))
        html.add(HTMLObjects.HTMLTableCell(event_link))
        return html

    def _role_description(self, appointment):
        roleDescription = appointment.role.description
        if appointment.note is not None and len(appointment.note) > 0 and appointment.note is not 'None':
            roleDescription += '('
            roleDescription += appointment.note
            roleDescription += ')'
        return HTMLObjects.HTMLLink(roleDescription, "../roles/" + appointment.role.description + ".html")

    def _html_table_header_row(self):
        html = HTMLObjects.HTMLTableRow()
        html.add(HTMLObjects.HTMLTableHeaderCell('Date'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Time'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Role'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Event'))
        return html

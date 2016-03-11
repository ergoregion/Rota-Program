__author__ = 'Neil Butcher'

from Rota_System.Reporting.HTMLObjects import HTMLObjects
from Abstract import AbstractMultiAppointmentReporter, event_title, person_code
from Rota_System.StandardTimes import time_string, date_string


class RolesReporter(object):
    def events(self, events):
        self._reporter = RoleReporter()
        self._reporter.events(events)

    def write_reports_about(self, a_list, a_folder):
        if not self._reporter.events:
            return HTMLObjects.HTMLNone()
        self._write_index_file(a_list, a_folder)
        for role in a_list:
            html = self._reporter.report_about(role)
            filename = a_folder + '\\' + role.description + '.html'
            fileopen = open(filename, 'w')
            fileopen.write(html.html_string())
            fileopen.close()

    def _write_index_file(self, a_list, a_folder):

        table = HTMLObjects.HTMLTable()
        for role in sorted(a_list, key=lambda r: r.description):
            text = HTMLObjects.HTMLLink(role.description, "./" + role.description + ".html")
            cell = HTMLObjects.HTMLTableCell(text)
            row = HTMLObjects.HTMLTableRow(cell)
            table.add(row)

        html = HTMLObjects.HTMLAll(HTMLObjects.HTMLHead(HTMLObjects.HTMLPageTitle('Roles')))
        html.add(HTMLObjects.HTMLLink("index", "../index.html"))
        html.add(HTMLObjects.HTMLTitle('Roles'))
        html.add(table)
        filename = a_folder + '\\' + 'index.html'
        fileopen = open(filename, 'w')
        fileopen.write(html.html_string())
        fileopen.close()


class RoleReporter(AbstractMultiAppointmentReporter):
    '''
    produces a html from a role and a list of events
    '''

    def report_about(self, an_object):
        if not self._events:
            return HTMLObjects.HTMLNone()
        self.role(an_object)
        return self.html()

    def role(self, role):

        self._all_appointments = set()
        self._role = role
        for e in self._events:
            correct_appointments = filter(lambda x: x.role == role, e.appointments)
            self._all_appointments.update(correct_appointments)

    def _html_preheader(self):
        return HTMLObjects.HTMLLink("roles", "./index.html")

    def _html_header(self):
        return HTMLObjects.HTMLTitle(self._role.description)

    def _html_table(self):
        table = HTMLObjects.HTMLTable()
        row = HTMLObjects.HTMLTableRow()
        row.add(HTMLObjects.HTMLTableHeaderCell("Date"))
        row.add(HTMLObjects.HTMLTableHeaderCell("Time"))
        row.add(HTMLObjects.HTMLTableHeaderCell("Event"))
        row.add(HTMLObjects.HTMLTableHeaderCell("People"))
        table.add(row)
        for e in sorted(self._events, key=lambda e: e.datetime()):
            correct_appointments = [a for a in self._all_appointments if e is a.event]
            if len(correct_appointments) > 0:
                link = HTMLObjects.HTMLLink(e.title, "../events/" + event_title(e) + ".html")
                row = HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableHeaderCell(date_string(e.date)))
                row.add(HTMLObjects.HTMLTableHeaderCell(time_string(e.time)))
                row.add(HTMLObjects.HTMLTableHeaderCell(link))
                names = map(person_name, correct_appointments)
                if len(names) > 0:
                    string = '<br>'.join(names)
                else:
                    string = ''
                row.add(HTMLObjects.HTMLTableCell(string))
                table.add(row)
        return table


def person_name(an_object):
    if an_object.is_filled():
        link = HTMLObjects.HTMLLink(person_code(an_object.person), "../people/" + person_code(an_object.person) + ".html")
        return link.html_string()
    else:
        return 'Not filled'

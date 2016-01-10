__author__ = 'Neil Butcher'

from HTMLObjects import HTMLObjects
from Rota_System.StandardTimes import date_string, time_string


class EventReporter(object):
    def event(self, event):
        self._event = event

    def report_about(self, anObject):
        self.event(anObject)
        return self.html().html_string()

    def html(self):
        if len(self._event.appointments) == 0:
            return HTMLObjects.HTMLNone()
        html = HTMLObjects.HTMLGroup()
        html.add(self._html_header())
        html.add(self._html_table())
        html.add(self._html_footer())
        return html

    def _html_header(self):
        title = 'Event '
        title += date_string(self._event.date)
        title += '   '
        title += time_string(self._event.time)
        return HTMLObjects.HTMLHeading(title)

    def _html_table(self):
        table = HTMLObjects.HTMLTable()
        table.add(self._html_table_row_header())
        sorted_appointments = sorted(self._event.appointments, key=lambda app: app.role.priority, reverse=True)
        for appointment in sorted_appointments:
            table.add(self._html_table_row(appointment))
        return table

    def _html_footer(self):
        return None

    def _html_table_row_header(self):
        html = HTMLObjects.HTMLTableRow()
        html.add(HTMLObjects.HTMLTableHeaderCell('Role'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Person'))
        html.add(HTMLObjects.HTMLTableHeaderCell('Phone Number'))
        html.add(HTMLObjects.HTMLTableHeaderCell('email'))
        html.add(HTMLObjects.HTMLTableHeaderCell('note'))
        return html

    def _html_table_row(self, appointment):
        html = HTMLObjects.HTMLTableRow()
        if appointment.disabled and not (appointment.isFilled()):
            return None
        html.add(HTMLObjects.HTMLTableCell(appointment.role.description))
        if appointment.isFilled():
            html.add(HTMLObjects.HTMLTableCell(appointment.person.name))
            html.add(HTMLObjects.HTMLTableCell(appointment.person.phoneNumber))
            html.add(HTMLObjects.HTMLTableCell(appointment.person.email))
        else:
            html.add(HTMLObjects.HTMLTableCell('Not filled', 3, 1))
        html.add(HTMLObjects.HTMLTableCell(appointment.note))
        return html

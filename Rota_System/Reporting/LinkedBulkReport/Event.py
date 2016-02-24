__author__ = 'Neil Butcher'

from Rota_System.Reporting.HTMLObjects import HTMLObjects
from Abstract import event_title
from Rota_System.StandardTimes import date_string, time_string


class EventsReporter(object):

    def write_reports_about(self, a_list, a_folder):

        self._reporter = EventReporter()

        titles = []
        for event in a_list:
            html = self._reporter.report_about(event)
            et = event_title(event)
            filename = a_folder + '\\' + et + '.html'
            fileopen = open(filename,'w')
            fileopen.write(html.html_string())
            fileopen.close()
            titles.append(et)
        self._write_index_file(titles, a_folder)

    def _write_index_file(self, a_list, a_folder):

        table = HTMLObjects.HTMLTable()
        for event_title in a_list :
            text = HTMLObjects.HTMLLink(event_title, "./" + event_title + ".html")
            cell = HTMLObjects.HTMLTableCell(text)
            row = HTMLObjects.HTMLTableRow(cell)
            table.add(row)

        html = HTMLObjects.HTMLAll(HTMLObjects.HTMLHead(HTMLObjects.HTMLPageTitle('Events')))
        html.add(HTMLObjects.HTMLLink("index", "../index.html"))
        html.add(HTMLObjects.HTMLTitle('Events'))
        html.add(table)
        filename = a_folder + '\\' + 'index.html'
        fileopen = open(filename,'w')
        fileopen.write(html.html_string())
        fileopen.close()

class EventReporter(object):
    def event(self, event):
        self._event = event

    def report_about(self, an_object):
        self.event(an_object)
        return self.html()

    def html(self):

        html = HTMLObjects.HTMLGroup()
        html.add(self._html_preheader())
        html.add(self._html_header())
        if len(self._event.appointments) > 0:
            html.add(self._html_table())
        html.add(self._html_footer())
        return html

    def title(self):
        return event_title(self._event)

    def _html_preheader(self):
        return HTMLObjects.HTMLLink("events", "./index.html")

    def _html_header(self):
        title = 'Event '
        title += event_title(self._event)
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
        if appointment.disabled and not (appointment.is_filled()):
            return None
        link =  HTMLObjects.HTMLLink(appointment.role.description, "../roles/" + appointment.role.description + ".html")
        html.add(HTMLObjects.HTMLTableCell(link))
        if appointment.is_filled():
            link =  HTMLObjects.HTMLLink(appointment.person.name, "../people/" + appointment.person.name + ".html")
            html.add(HTMLObjects.HTMLTableCell(link))
            html.add(HTMLObjects.HTMLTableCell(appointment.person.phone_number))
            html.add(HTMLObjects.HTMLTableCell(appointment.person.email))
        else:
            html.add(HTMLObjects.HTMLTableCell('Not filled', 3, 1))
        html.add(HTMLObjects.HTMLTableCell(appointment.note))
        return html

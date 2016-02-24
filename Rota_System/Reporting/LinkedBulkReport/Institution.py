__author__ = 'Neil Butcher'

from Rota_System.Reporting.HTMLObjects import HTMLObjects
from Person import PopulationReporter
from Role import RolesReporter
from Event import EventsReporter
from Rota_System.Roles import GlobalRoleList
import os


class DurationReporter(object):
    def write_reports_about(self, an_institution, a_duration, a_folder):
        self._population_reporter = PopulationReporter()
        self._population_reporter.events(a_duration.events)
        if not os.path.exists(a_folder + '\\people'):
            os.makedirs(a_folder + '\\people')
        self._population_reporter.write_reports_about(an_institution.people, a_folder + '\\people')
        self._roles_reporter = RolesReporter()
        self._roles_reporter.events(a_duration.events)
        if not os.path.exists(a_folder + '\\roles'):
            os.makedirs(a_folder + '\\roles')
        self._roles_reporter.write_reports_about(GlobalRoleList.roles, a_folder + '\\roles')
        self._events_reporter = EventsReporter()
        if not os.path.exists(a_folder + '\\events'):
            os.makedirs(a_folder + '\\events')
        self._events_reporter.write_reports_about(a_duration.events, a_folder + '\\events')
        self._write_index_file(a_duration, a_folder)

    def _write_index_file(self, a_duration, a_folder):

        table = HTMLObjects.HTMLTable()
        text = HTMLObjects.HTMLLink('People', "./people/index.html")
        table.add(HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableCell(text)))
        text = HTMLObjects.HTMLLink('Roles', "./roles/index.html")
        table.add(HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableCell(text)))
        text = HTMLObjects.HTMLLink('Events', "./events/index.html")
        table.add(HTMLObjects.HTMLTableRow(HTMLObjects.HTMLTableCell(text)))

        html = HTMLObjects.HTMLAll(HTMLObjects.HTMLHead(HTMLObjects.HTMLPageTitle(a_duration.name)))
        html.add(HTMLObjects.HTMLTitle(a_duration.name))
        html.add(table)
        filename = a_folder + '\\' + 'index.html'
        fileopen = open(filename, 'w')
        fileopen.write(html.html_string())
        fileopen.close()

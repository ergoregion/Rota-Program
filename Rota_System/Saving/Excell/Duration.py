__author__ = 'Neil Butcher'

from Error import ExcellImportExportError
from Rota_System.StandardTimes import date_string, time_string, get_date, get_time
import xlwt, xlrd
from Rota_System.Roles import GlobalRoleList, role
from Rota_System.Events import Event


def _job(appointment):
    return appointment.role.description, appointment.note


styleInvalid = xlwt.easyxf('pattern: pattern solid, fore_colour  gray25;')
styleDisabled = xlwt.easyxf('font: colour red;')


class DurationSavingObject(object):
    def __init__(self, duration, filename):
        if filename:
            self._filename = filename
        else:
            raise ExcellImportExportError('No filename set')

        self._duration = duration
        self._book = None

    def _save(self):
        self._book.save(self._filename)

    def create(self):

        self._book = xlwt.Workbook(encoding="utf-8")
        self._event_sheet = self._book.add_sheet("Events")

        self._event_sheet.write(0, 0, 'Date')
        self._event_sheet.write(0, 1, 'Time')
        self._event_sheet.write(0, 2, 'Title')
        self._event_sheet.write(0, 3, 'Notes')
        self._event_sheet.write(0, 4, 'Description')

        self._vacancies_sheets = {}
        for r in GlobalRoleList.roles:
            self._vacancies_sheets[r.description] = self._book.add_sheet(r.description)
            self._vacancies_sheets[r.description].write(1, 0, 'note')

        jobs = self._gather_jobs()
        for d in jobs:
            for i, j in enumerate(jobs[d]):
                sheet = self._vacancies_sheets[j[0]]
                sheet.write(0, i + 1, str(i + 1))
                sheet.write(1, i + 1, j[1])

        self._save()

    def _gather_jobs(self):

        self._jobs = {}
        for e in self._duration.events:
            event_jobs = map(_job, e.appointments)
            for e_j in event_jobs:
                d = e_j[0]
                if d not in self._jobs:
                    self._jobs[d] = []
                if self._jobs[d].count(e_j) < event_jobs.count(e_j):
                    self._jobs[d].append(e_j)
        return self._jobs

    def _add_event(self, event, row):

        self._event_sheet.write(row, 0, date_string(event.date))
        self._event_sheet.write(row, 1, time_string(event.time))
        self._event_sheet.write(row, 2, event.title)
        self._event_sheet.write(row, 3, event.notes)
        self._event_sheet.write(row, 4, event.description)

        for r in GlobalRoleList.roles:
            self._vacancies_sheets[r.description].write(row, 0, event.title + '(' + date_string(event.date) + ')')

        event_jobs = map(_job, event.appointments)
        for d in self._jobs:
            for i, j in enumerate(self._jobs[d]):
                try:
                    index = event_jobs.index(j)
                    appointment = event.appointments[index]
                    if appointment.disabled:
                        self._vacancies_sheets[j[0]].write(row, i + 1, "Disabled", styleDisabled)
                    elif appointment.is_filled():
                        self._vacancies_sheets[j[0]].write(row, i + 1, appointment.person.name)
                    else:
                        self._vacancies_sheets[j[0]].write(row, i + 1, "")

                    event_jobs[index] = None

                except ValueError:
                    self._vacancies_sheets[j[0]].write(row, i + 1, "", styleInvalid)

    def populate(self):
        for j, e in enumerate(self._duration.events):
            self._add_event(e, j + 2)
        self._save()

    def load_events(self):
        self._book = xlrd.open_workbook(self._filename)
        self._get_sheets(just_events=True)
        self._get_events()
        return self._duration.events

    def load(self, population=[]):
        self._book = xlrd.open_workbook(self._filename)
        self._get_sheets()
        self._fill_appointments(population)
        return self._duration

    def _get_sheets(self, just_events=False):
        names = self._book.sheet_names()
        if "Events" not in names:
            raise ExcellImportExportError('There is no events sheet in the file')
        else:
            self._event_sheet = self._book.sheet_by_name("Events")

        if just_events:
            return self

        self._vacancies_sheets = {}
        for r in GlobalRoleList.roles:
            if r.description not in names:
                raise ExcellImportExportError('There is no vacancies sheet in the file about' + r.description)
            else:
                self._vacancies_sheets[r.description] = self._book.sheet_by_name(r.description)

    def _get_events(self):
        if len(self._duration.events) > 0:
            raise ExcellImportExportError('This duration already has events')

        self._duration.events = []

        table_events = []
        for i in range(2, self._event_sheet.nrows):
            if self._event_sheet.cell_type(i, 0) is 0:
                break
            else:
                e = {}
                e['date'] = self._event_sheet.cell_value(i, 0)
                e['time'] = self._event_sheet.cell_value(i, 1)
                e['title'] = self._event_sheet.cell_value(i, 2)
                e['notes'] = self._event_sheet.cell_value(i, 3)
                e['description'] = self._event_sheet.cell_value(i, 4)
                table_events.append(e)

        for e in table_events:
            event = Event(self._duration)
            event.title = e['title']
            event.notes = e['notes']
            event.description = e['description']
            event.date = get_date(e['date'])
            event.time = get_time(e['time'])
            self._duration.events.append(event)

    def _get_events_order(self):

        if self._event_sheet.nrows - 2 != len(self._duration.events):
            raise ExcellImportExportError('There are the wrong number of event entries on the events sheet')

        table_events = []
        for i in range(2, self._event_sheet.nrows):
            if self._event_sheet.cell_type(i, 0) is 0:
                break
            else:
                e = {}
                e['date'] = self._event_sheet.cell_value(i, 0)
                e['time'] = self._event_sheet.cell_value(i, 1)
                e['title'] = self._event_sheet.cell_value(i, 2)
                e['notes'] = self._event_sheet.cell_value(i, 3)
                e['description'] = self._event_sheet.cell_value(i, 4)
                table_events.append(e)

        ordered_events = [None for _ in range(len(self._duration.events))]

        for event in self._duration.events:
            for i, e in enumerate(table_events):
                if e is not None:
                    if e['title'] == event.title and e['notes'] == event.notes and e[
                        'description'] == event.description:
                        if e['date'] == date_string(event.date) and e['time'] == time_string(event.time):
                            ordered_events[i] = event
                            table_events[i] = None

        if None in ordered_events:
            raise ExcellImportExportError('Not all the events of the duration were incoprorated in the sheet')
        for e in table_events:
            if e is not None:
                raise ExcellImportExportError('Not all the events of the sheet were present in the duration')

        for s in self._vacancies_sheets:
            for i, e in enumerate(ordered_events):
                if self._vacancies_sheets[s].cell_value(i + 2, 0) != e.title + '(' + date_string(e.date) + ')':
                    raise ExcellImportExportError('The sheet about ' + s + ' did not have the matching events')

        return ordered_events

    def _fill_appointments(self, population):

        ordered_events = self._get_events_order()

        for r in GlobalRoleList.roles:
            sheet = self._vacancies_sheets[r.description]
            for ei, event in enumerate(ordered_events):
                row_index = ei + 2
                row = sheet.row(row_index)
                appointments = [a for a in event.appointments if a.role is r]
                cell_entries = [(sheet.cell_value(1, i), sheet.cell_value(row_index, i)) for i in range(1, len(row)) if
                                sheet.cell_type(row_index, i) is not 0]

                for c in cell_entries:
                    noted_filled_appointments = [a for a in appointments if
                                                 a.note == c[0] and not a.disabled and a.is_filled()]
                    noted_disabled_appointments = [a for a in appointments if a.note == c[0] and a.disabled]
                    noted_vacant_appointments = [a for a in appointments if
                                                 a.note == c[0] and not a.disabled and not a.is_filled()]

                    if c[1] == 'Disabled':
                        if len(noted_disabled_appointments) > 0:
                            appointments.remove(noted_disabled_appointments[0])
                        elif len(noted_vacant_appointments) > 0:
                            noted_vacant_appointments[0].disabled = True
                            appointments.remove(noted_vacant_appointments[0])
                        else:
                            raise ExcellImportExportError('There is no vacant appointment to disable')
                    else:
                        name = c[1]
                        people = [p for p in population if p.name == name]
                        if len(people) > 1:
                            raise ExcellImportExportError('There are multiple people with the name ' + name)
                        elif len(people) == 0:
                            raise ExcellImportExportError('There is nobody with the name ' + name)
                        else:
                            person = people[0]

                        ready_filled_appointments = [a for a in noted_filled_appointments if a.person is person]
                        if len(ready_filled_appointments) > 0:
                            appointments.remove(ready_filled_appointments[0])
                        elif len(noted_vacant_appointments) > 0:
                            noted_vacant_appointments[0].appoint(person)
                            appointments.remove(noted_vacant_appointments[0])
                        else:
                            raise ExcellImportExportError('There is no vacant appointment to fill')

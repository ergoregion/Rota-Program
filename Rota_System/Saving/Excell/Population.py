__author__ = 'Neil Butcher'

from Error import ExcellImportExportError
import xlwt, xlrd
from Rota_System.Roles import GlobalRoleList, role
from datetime import datetime
from Rota_System.Worker import Worker


class PopulationSavingObject(object):
    def __init__(self, population, filename):
        if filename:
            self._filename = filename
        else:
            raise ExcellImportExportError('No filename set')

        self._population = population
        self._book = None

    def create(self):

        self._book = xlwt.Workbook(encoding="utf-8")
        self._population_sheet = self._book.add_sheet("Population")

        self._population_sheet.write(0, 0, 'Name')
        self._population_sheet.write(0, 1, 'phone')
        self._population_sheet.write(0, 2, 'email')
        self._population_sheet.write(0, 3, 'address')

        self._qualifications_sheet = self._book.add_sheet("Qualifications")
        self._qualifications_sheet.write(0, 0, 'Name')
        j = 1
        for r in GlobalRoleList.roles:
            self._qualifications_sheet.write(0, j, r.description)
            j += 1

        self._dates_sheet = self._book.add_sheet("Unavailable Dates")
        self._dates_sheet.write(0, 0, 'Name')
        self._save()

    def _add_individual(self, person, row):

        self._population_sheet.write(row, 0, person.name)
        self._population_sheet.write(row, 1, person.phone_number)
        self._population_sheet.write(row, 2, person.email)
        self._population_sheet.write(row, 3, person.address)

        self._qualifications_sheet.write(row, 0, person.name)
        self._dates_sheet.write(row, 0, person.name)

        j = 1
        for r in GlobalRoleList.roles:
            if person.suitable_for_role(r):
                self._qualifications_sheet.write(row, j, "Y")
            j += 1

        j = 1
        for d in person.blacklisted_dates():
            self._dates_sheet.write(row, j, str(d))
            j += 1

    def populate(self):
        for j, person in enumerate(self._population):
            self._add_individual(person, j + 1)
        self._save()

    def _save(self):
        self._book.save(self._filename)

    def load(self):
        self._book = xlrd.open_workbook(self._filename)
        self._get_sheets()
        self._get_roles()
        self._get_people()
        return self._population

    def _get_sheets(self):
        names = self._book.sheet_names()
        if "Population" not in names:
            raise ExcellImportExportError('There is no population sheet in the file')
        else:
            self._population_sheet = self._book.sheet_by_name("Population")
        if "Qualifications" not in names:
            raise ExcellImportExportError('There is no qualification sheet in the file')
        else:
            self._qualifications_sheet = self._book.sheet_by_name("Qualifications")

        if "Unavailable Dates" in names:
            self._dates_sheet = self._book.sheet_by_name("Unavailable Dates")
        else:
            self._dates_sheet = None

    def _get_roles(self):
        self._sheet_role_list = []

        for i, cell in enumerate(self._qualifications_sheet.row(0)):

            if cell.ctype is 0:
                break
            try:
                r = role(cell.value)
            except:
                raise ExcellImportExportError('There was an unidentified role: ' + cell.value)
            if r is None:
                if i > 0:
                    raise ExcellImportExportError('There was an unidentified role: ' + cell.value)
            else:
                self._sheet_role_list.append(r)

        for r in GlobalRoleList.roles:
            if r not in self._sheet_role_list:
                raise ExcellImportExportError('There was an role unlisted on the sheet: ' + r.description)

    def _get_people(self):
        self._population = []

        for i in range(1, self._population_sheet.nrows):
            if self._population_sheet.cell_type(i, 0) is 0:
                break
            else:
                p = Worker()
                p.name = self._population_sheet.cell_value(i, 0)
                p.phone_number = self._population_sheet.cell_value(i, 1)
                p.email = self._population_sheet.cell_value(i, 2)
                p.address = self._population_sheet.cell_value(i, 3)
                self._get_qualifications(i, p)
                self._get_dates(i, p)
                self._population.append(p)

    def _get_qualifications(self, row, person):
        cells = self._qualifications_sheet.row(row)

        if cells[0].value != person.name:
            raise ExcellImportExportError('There was a mismatch between people and qalifications on row: ' + str(row))

        person.does_nothing()

        for i, r in enumerate(self._sheet_role_list):
            if cells[i + 1].ctype is not 0:
                person.add_role(r.code)

    def _get_dates(self, row, person):
        if self._dates_sheet is None:
            return
        cells = self._dates_sheet.row(row)

        if cells[0].value != person.name:
            raise ExcellImportExportError('There was a mismatch between people and qualifications on row: ' + str(row))

        person.clear_blacklist()

        for i in range(1, len(cells)):
            if cells[i].ctype is not 0:
                person.blacklist_date(get_date(cells[i].value))


def get_date(a_string):
    return (datetime.strptime(a_string, "%Y-%m-%d")).date()

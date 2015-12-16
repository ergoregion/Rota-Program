__author__ = 'Neil Butcher'

from Person import Person
from Roles import RoleList, role


class Worker(Person):

    def __init__(self, parent=None):
        Person.__init__(self, parent)
        self._roles = RoleList('', self)

    def does_nothing(self):
        self._roles = RoleList()
        return self

    def number_of_roles(self):
        return self._roles.number_of_roles()

    def add_role(self, role_code_or_desc):
        r = role(role_code_or_desc)
        self._roles.add(r)

    def add_roles(self, strings):
        codes = strings.split()
        for code in codes:
            self._roles.add_code(code)

    def remove_role(self, role_code_or_desc):
        r = role(role_code_or_desc)
        self._roles.remove(r)

    def remove_roles(self, strings):
        codes = strings.split()
        for code in codes:
            self._roles.remove_code(code)

    def suitable_for_role(self, a_role):
        return self._roles.includes(a_role)

    def roles(self):
        return self._roles.roles
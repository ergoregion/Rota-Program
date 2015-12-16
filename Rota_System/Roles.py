__author__ = 'Neil Butcher'

from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal, QObject


class UndefinedRoleError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'This is an invalid role ', self.value


def role(role_code_desc):
    if role_code_desc in GlobalRoleList.roles:
        return role_code_desc
    try:
        return GlobalRoleList.role_from_code(role_code_desc)
    except UndefinedRoleError:
        try:
            return GlobalRoleList.role_from_desc(role_code_desc)
        except UndefinedRoleError:
            return None


def role_from_code(code):
    return GlobalRoleList.role_from_code(code)


def role_from_desc(desc):
    return GlobalRoleList.role_from_desc(desc)


def roles_from_codes(codes):
    return map((lambda code: role_from_code(code)), codes.split())


class Role(QObject):
    compatibilitiesChanged = pyqtSignal()
    descriptionChanged = pyqtSignal(str)
    priorityChanged = pyqtSignal(int)

    def strip(self):
        return self.code.strip()

    def __str__(self):
        return self.description

    def equals(self, a_role):
        if self == a_role:
            return True
        if self.code == a_role.strip():
            return True
        return self.code == a_role.code.strip()

    def __init__(self, desc, code, pri, parent=None):
        super(Role, self).__init__(parent)
        self._description = desc
        self.code = code
        self._priority = pri
        self.compatibilities = RoleList('', self)
        self.compatibilities.rolesChanged.connect(self._compatibilities_changed)

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value
        self.descriptionChanged.emit(value)

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        self._priority = value
        self.priorityChanged.emit(value)

    @QtCore.pyqtSlot()
    def _compatibilities_changed(self):
        self.compatibilitiesChanged.emit()

    def compatible_with(self, role2):
        return self.compatibilities.includes(role2)


class GlobalRoleListClass(QObject):
    roles = []
    roleAdded = pyqtSignal(str)
    roleRemoved = pyqtSignal(str)
    rolesCleared = pyqtSignal()
    rolesChanged = pyqtSignal()

    def clear(self):
        self.rolesCleared.emit()
        self.roles = []
        self.rolesChanged.emit()

    def add_role(self, new_role):
        self.roles.append(new_role)
        new_role.descriptionChanged.connect(self._emit_roles_changed)
        self.roleAdded.emit(new_role.code)
        self.rolesChanged.emit()

    def remove_role(self, removed_role):
        removed_role.descriptionChanged.disconnect(self._emit_roles_changed)
        self.roles.remove(removed_role)
        self.roleRemoved.emit(removed_role.code)
        self.rolesChanged.emit()

    def _emit_roles_changed(self):
        self.rolesChanged.emit()

    def role_from_code(self, code):
        stripped_code = code.strip()
        possibilities = filter((lambda a: a.code == stripped_code), self.roles)
        if len(possibilities) == 0:
            raise UndefinedRoleError(code)
        else:
            return possibilities[0]

    def role_from_desc(self, desc):
        desc = desc.strip()
        possibilities = filter((lambda a: a.description == desc), self.roles)
        if len(possibilities) == 0:
            raise UndefinedRoleError(desc)
        else:
            return possibilities[0]

    def new_code(self):

        for i in range(len(self.roles) + 1):
            a = str(i)
            try:
                self.roleFromCode(a)
            except UndefinedRoleError:
                return a


GlobalRoleList = GlobalRoleListClass()


class RoleList(QObject):
    rolesChanged = pyqtSignal()

    def __init__(self, args='', parent=None):
        super(RoleList, self).__init__(parent)
        self.roles = set()
        self.populate_from_codes(args)
        GlobalRoleList.rolesCleared.connect(self.none)
        GlobalRoleList.roleRemoved.connect(self.remove_code)
        GlobalRoleList.roleAdded.connect(self.rolesChanged)
        GlobalRoleList.rolesChanged.connect(self.rolesChanged)

    def all(self):
        self.roles = set()
        self.roles.update(GlobalRoleList.roles)
        self.rolesChanged.emit()

    @QtCore.pyqtSlot()
    def none(self):
        self.roles = set()
        self.rolesChanged.emit()

    def role_from_code(self, code):
        stripped_code = code.strip()
        possibilities = filter((lambda a: a.code == stripped_code), self.roles)
        if len(possibilities) == 0:
            raise UndefinedRoleError(code)
        else:
            return possibilities.pop()

    def role_from_desc(self, desc):
        desc = desc.strip()
        possibilities = filter((lambda a: a.description == desc), self.roles)
        if len(possibilities) == 0:
            raise UndefinedRoleError(desc)
        else:
            return possibilities.pop()

    def includes(self, role_or_code):
        if role_or_code in self.roles:
            return True
        try:
            self.role_from_code(role_or_code)
        except UndefinedRoleError:
            try:
                self.role_from_desc(role_or_code)
            except UndefinedRoleError:
                return False
            return True
        return True

    def add(self, a_role):
        if a_role not in self.roles:
            self.roles.add(a_role)
            self.rolesChanged.emit()

    def remove(self, a_role):
        if a_role in self.roles:
            self.roles.remove(a_role)
            self.rolesChanged.emit()

    @QtCore.pyqtSlot(str)
    def add_code(self, code):
        for a_role in GlobalRoleList.roles:
            if a_role.code == code.strip():
                self.roles.add(a_role)
        self.rolesChanged.emit()

    @QtCore.pyqtSlot(str)
    def remove_code(self, code):
        try:
            r = self.role_from_code(code)
        except UndefinedRoleError:
            return self
        self.remove(r)

    def populate_from_codes(self, array_of_strings):
        self.roles = set()
        codes = array_of_strings.split()
        for code in codes:
            self.add_code(code)
        self.rolesChanged.emit()

    def list_of_codes(self):
        result = ''
        for a_role in self.roles:
            result = ' '.join([result, a_role.code])
        return result

    def number_of_roles(self):
        return len(self.roles)

    def _clean(self):
        new_roles = filter((lambda a_role: (self.includes(a_role))), GlobalRoleList.roles)
        self.roles = new_roles
        return self


GlobalRoleList.clear()
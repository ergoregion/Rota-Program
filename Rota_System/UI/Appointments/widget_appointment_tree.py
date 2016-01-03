__author__ = 'Neil Butcher'

from PyQt4 import QtCore, QtGui
from Rota_System.StandardTimes import time_string, date_string
from Rota_System.Roles import GlobalRoleList
from sets import Set


def is_vacant(appointment):
    return (not appointment.isFilled()) and (not appointment.disabled)


class _AppointmentsTreeRefreshCollectionObject(QtCore.QObject):
    """a bodge object to recieve many signals and report them to one tree widget.
    It can be destroyed to break all signals"""
    signalRefresh = QtCore.pyqtSignal()
    signalVacancyChanged = QtCore.pyqtSignal()

    @QtCore.pyqtSlot()
    def refresh(self):
        self.signalRefresh.emit()

    @QtCore.pyqtSlot()
    def vacancy_changed(self):
        self.signalVacancyChanged.emit()


class AppointmentsTreeListWidget(QtGui.QWidget):
    appointmentSelected = QtCore.pyqtSignal(QtCore.QObject)
    checkedChanged = QtCore.pyqtSignal(int, int)
    vacantAppointmentsChanged = QtCore.pyqtSignal(int, int)

    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)

        self.showCheckBoxes = False
        self.vacanciesOnly = False

        self._eventsModel = None
        self.layout = QtGui.QVBoxLayout(self)
        self.treeWidget = QtGui.QTreeWidget(self)
        self.treeWidget.itemChanged.connect(self._tree_item_changed)
        self.treeWidget.itemClicked.connect(self._tree_item_clicked)
        self.treeWidget.setHeaderHidden(True)
        refresh_button = QtGui.QPushButton(self)
        refresh_button.clicked.connect(self._refresh)
        refresh_button.setText('Refresh')
        refresh_button.setFixedWidth(200)
        self.layout.addWidget(self.treeWidget)
        self.layout.addWidget(refresh_button, alignment=QtCore.Qt.AlignCenter)

        self._roles_Item = self._add_parent(self.treeWidget, 0, 'roles')
        self._roles_Item.appointment = None
        self._events_Item = self._add_parent(self.treeWidget, 0, 'events')
        self._events_Item.appointment = None

        GlobalRoleList.rolesChanged.connect(self._refresh)
        self._collectingObject = None

    def eventsModel(self, eventModel):
        self._events = eventModel.events
        self._eventsModel = eventModel
        self._refresh()
        self._refresh_connections()
        eventModel.rowsInserted.connect(self._refresh_connections)
        eventModel.rowsRemoved.connect(self._refresh_connections)
        eventModel.rowsInserted.connect(self._refresh)
        eventModel.rowsRemoved.connect(self._refresh)

    @QtCore.pyqtSlot()
    def _refresh_connections(self):
        if self._collectingObject:
            self._collectingObject.signalRefresh.disconnect(self._refresh)
            self._collectingObject.deleteLater()
        self._collectingObject = _AppointmentsTreeRefreshCollectionObject(self)
        self._collectingObject.signalRefresh.connect(self._refresh)
        self._collectingObject.signalVacancyChanged.connect(self._signal_vacancy_changed)
        GlobalRoleList.rolesChanged.connect(self._collectingObject.refresh)
        self._eventsModel.dataChanged.connect(self._collectingObject.refresh)
        for e in self._events:
            e.appointmentsChanged.connect(self._collectingObject.refresh)
            e.appointmentsChanged.connect(self._collectingObject.vacancy_changed)

    @QtCore.pyqtSlot()
    def _refresh(self):
        if self._eventsModel is not None:
            self._cache_enabled_appointments()
            self._refresh_roles_children()
            self._refresh_events_children()
            self._restore_enabled_appointment()

    def _cache_enabled_appointments(self):
        self._currentlyEnabledStash = self.checkedAppointments()

    def _restore_enabled_appointment(self):
        self._restore_checked_items(self.treeWidget.invisibleRootItem())
        self._currentlyEnabledStash = None
        self.checkedChanged.emit(len(self.checkedAppointments()), len(self.checkedVacantAppointments()))

    def _refresh_roles_children(self):

        self._rolesItemsDict = {}

        self._roles_Item.takeChildren()
        for role in sorted(GlobalRoleList.roles, key=lambda r: r.priority, reverse=True):
            role_item = self._add_child(self._roles_Item, 0, str(role))

            role_item.appointment = None
            self._rolesItemsDict[role] = role_item

    def _refresh_events_children(self):

        self._events_Item.takeChildren()
        date = None
        date_item = None
        for event in sorted(self._events, key=lambda w: w.datetime):

            if not event.date == date:
                date = event.date
                date_item = self._add_child(self._events_Item, 0, date_string(date))
                date_item.appointment = None

            event_item = self._add_child(date_item, 0, event.name)

            event_item.appointment = None

            appointment_list = event.appointments
            if self.vacanciesOnly:
                appointment_list = filter(is_vacant, appointment_list)

            for appointment in appointment_list:
                appointment.changed.connect(self._collectingObject.vacancy_changed)
                appointment_item = self._add_child(event_item, 0, str(appointment.role) + '(' + appointment.note + ')')

                appointment_item.appointment = appointment

                this_item = self._add_child(self._rolesItemsDict[appointment.role], 0, event.title + '(' + date_string(
                    event.date) + ')' + '(' + appointment.note + ')')
                this_item.appointment = appointment

    def _add_parent(self, parent, column, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        if self.showCheckBoxes:
            item.setCheckState(column, QtCore.Qt.Unchecked)
        item.setExpanded(True)
        return item

    def _add_child(self, parent, column, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        if self.showCheckBoxes:
            item.setCheckState(column, QtCore.Qt.Unchecked)
        return item

    def _tree_item_changed(self, item):

        row_count = item.childCount()
        for i in range(0, row_count):
            item.child(i).setCheckState(0, item.checkState(0))
        self.checkedChanged.emit(len(self.checkedAppointments()), len(self.checkedVacantAppointments()))

    def _tree_item_clicked(self, tree_widget_item, i):
        self.appointmentSelected.emit(tree_widget_item.appointment)

    def checkedAppointments(self):
        appointments = Set()
        for treeItem in self._all_checked_tree_items():
            if treeItem.appointment:
                appointments.add(treeItem.appointment)
        return appointments

    def checkedVacantAppointments(self):
        appointments = Set()
        for treeItem in self._all_checked_tree_items():
            if treeItem.appointment:
                appointments.add(treeItem.appointment)
        return filter(is_vacant, appointments)

    def vacantAppointments(self):
        appointments = Set()
        for event in self._events:
            appointments.update(event.appointments)
        return filter(is_vacant, appointments)

    def appointments(self):
        appointments = Set()
        for event in self._events:
            appointments.update(event.appointments)
        return appointments

    def _signal_vacancy_changed(self):
        self.vacantAppointmentsChanged.emit(len(self.vacantAppointments()), len(self.checkedVacantAppointments()))

    def _all_checked_tree_items(self):
        li = []
        self.treeWidget.invisibleRootItem().appointment = None
        self._collect_checked_items(self.treeWidget.invisibleRootItem(), li)
        return li

    def _collect_checked_items(self, item, li):
        if item.checkState(0):
            li.append(item)
        for i in range(item.childCount()):
            self._collect_checked_items(item.child(i), li)

    def _restore_checked_items(self, item):
        if not self.showCheckBoxes:
            return self
        if item.appointment in self._currentlyEnabledStash:
            checked = QtCore.Qt.Checked
        else:
            checked = QtCore.Qt.Unchecked
        item.setCheckState(0, checked)
        for i in range(item.childCount()):
            self._restore_checked_items(item.child(i))


import sys


def main():


    app = QtGui.QApplication(sys.argv)
    w = AppointmentsTreeListWidget(None)
    w.show()


    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
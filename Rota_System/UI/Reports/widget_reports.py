__author__ = 'Neil Butcher'

import os
from PyQt4 import QtCore, QtGui, uic
from Rota_System.Roles import GlobalRoleList
from Rota_System import Reporting
from Rota_System.StandardTimes import date_string
from widget_webview import WebView
from Rota_System.Reporting.LinkedBulkReport import DurationReporter


class ReportWidget(QtGui.QWidget):
    def __init__(self, parent):
        QtGui.QWidget.__init__(self, parent)
        fn = os.path.join(os.path.dirname(__file__),'ReportWidget.ui')
        uic.loadUi(fn, self)
        self.reportBrowser = WebView(self)
        self.stackedWidget.addWidget(self.reportBrowser)
        self._roleReporter = Reporting.RoleReporter()
        self._eventReporter = Reporting.EventReporter()
        self._personReporter = Reporting.PersonReporter()

        self._roles_Item = self._add_parent(self.treeWidget, 0, 'roles')
        self._roles_Item.reportTupple = None

        self._people_item = self._add_parent(self.treeWidget, 0, 'People')
        self._people_item.reportTupple = None

        self._events_Item = self._add_parent(self.treeWidget, 0, 'events')
        self._events_Item.reportTupple = None

        self._refresh_roles_children()
        GlobalRoleList.rolesChanged.connect(self._refresh_roles_children)

        self.treeWidget.collapseAll()
        self.treeWidget.expandToDepth(0)

    def _refresh_roles_children(self):

        li = []
        self._collect_checked_items(self._roles_Item, li)
        enabled = map(lambda i: i.reportable[0], li)
        self._roles_Item.takeChildren()
        for role in sorted(GlobalRoleList.roles, key=lambda r: r.priority, reverse=True):
            item = self._add_child(self._roles_Item, 0, str(role))

            if role in enabled:
                checked = QtCore.Qt.Checked
            else:
                checked = QtCore.Qt.Unchecked

            item.setCheckState(0, checked)
            item.reportTupple = role, self._roleReporter

    def _refresh_people_children(self):

        li = []
        self._collect_checked_items(self._people_item, li)
        enabled = map(lambda item: item.reportable[0], li)
        self._people_item.takeChildren()
        for person in sorted(self._people, key=lambda w: w.name):
            item = self._add_child(self._people_item, 0, person.name)

            if person in enabled:
                checked = QtCore.Qt.Checked
            else:
                checked = QtCore.Qt.Unchecked

            item.setCheckState(0, checked)
            item.reportTupple = person, self._personReporter

    def _refresh_events_children(self):

        li = []
        self._collect_checked_items(self._events_Item, li)
        enabled = map(lambda i: i.reportable[0], li)
        self._events_Item.takeChildren()
        date = None
        date_item = None
        for event in sorted(self._events, key=lambda w: w.datetime):

            if not event.date == date:
                date = event.date
                date_item = self._add_child(self._events_Item, 0, date_string(date))
                date_item.reportTupple = None

            item = self._add_child(date_item, 0, event.name)

            if event in enabled:
                checked = QtCore.Qt.Checked
            else:
                checked = QtCore.Qt.Unchecked

            item.setCheckState(0, checked)
            item.reportTupple = event, self._eventReporter

    def selectedTreeItem(self, tree_widget_item, i):
        if tree_widget_item.reportTupple != None:
            reportTupple = tree_widget_item.reportTupple
            html = reportTupple[1].report_about(reportTupple[0])
            self.reportBrowser.setHtml(html)

    def treeItemChanged(self, item):
        rowCount = item.childCount()
        for i in range(0, rowCount):
            item.child(i).setCheckState(0, item.checkState(0))

    def setPopulationModel(self, population_model):
        self._people = population_model.population
        self._institution = population_model.institution
        self._refresh_people_children()
        population_model.dataChanged.connect(self._refresh_people_children)
        population_model.rowsInserted.connect(self._refresh_people_children)
        population_model.rowsRemoved.connect(self._refresh_people_children)

    def setEventsModel(self, event_model):
        self._events = event_model.events
        self._roleReporter.events(event_model.events)
        self._personReporter.events(event_model.events)
        self._refresh_events_children()
        self._duration = event_model.duration
        event_model.dataChanged.connect(self._refresh_events_children)
        event_model.rowsInserted.connect(self._refresh_events_children)
        event_model.rowsRemoved.connect(self._refresh_events_children)

    def _add_parent(self, parent, column, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setChildIndicatorPolicy(QtGui.QTreeWidgetItem.ShowIndicator)
        item.setCheckState(column, QtCore.Qt.Unchecked)
        item.setExpanded(True)
        return item

    def _add_child(self, parent, column, title):
        item = QtGui.QTreeWidgetItem(parent, [title])
        item.setCheckState(column, QtCore.Qt.Unchecked)
        return item

    @QtCore.pyqtSlot()
    def produceReports(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, 'Choose output folder')
        DurationReporter().write_reports_about(self._institution, self._duration, str(folder))

    @QtCore.pyqtSlot()
    def produceSelectedReports(self):
        items = self._all_checked_tree_reports()
        if len(items) == 0: return None
        folder = QtGui.QFileDialog.getExistingDirectory(self, 'Choose output folder')
        for i in items:
            if i.reportable != None:
                i.reportable.outputHTMLToFolder(folder)

    def _all_checked_tree_reports(self):
        li = []
        self._collect_checked_items(self.treeWidget.invisibleRootItem(), li)
        return li

    def _collect_checked_items(self, item, li):
        if item.checkState(0):
            li.append(item)
        for i in range(item.childCount()):
            self._collect_checked_items(item.child(i), li)

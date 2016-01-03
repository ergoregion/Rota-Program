__author__ = 'Neil Butcher'

from PyQt4 import QtGui


class PopulationSortFilterModel(QtGui.QSortFilterProxyModel):
    def __init__(self, parent):
        QtGui.QAbstractProxyModel.__init__(self, parent)
        self.setDynamicSortFilter(True)
        self._filters = []
        self._antifilters = []
        self._sorter = None

    def set_sorter(self, new_sorter):
        self._sorter = new_sorter
        self.invalidate()

    def clear_filters(self):
        self._filters = []
        self._antifilters = []
        self.invalidateFilter()

    def set_filters(self, new_filters):
        self._filters = new_filters
        self.invalidateFilter()

    def add_filter(self, new_filter):
        self._filters.append(new_filter)
        self.invalidateFilter()

    def add_reversed_filter(self, new_filter):
        self._antifilters.append(new_filter)
        self.invalidateFilter()

    def filter_accepts_row(self, source_row, source_parent):
        person = self.sourceModel().population[source_row]
        for f in self._filters:
            if f.mask(person):
                return False
        for f in self._antifilters:
            if not f.mask(person):
                return False
        return True

    def lessThan(self, left_index, right_index):
        if not self._sorter:
            return False
        left_person = self.sourceModel().object(left_index)
        right_person = self.sourceModel().object(right_index)
        return self._sorter.lessThan(left_person, right_person)

    def object(self, index):
        source_index = self.mapToSource(index)
        return self.sourceModel().object(source_index)

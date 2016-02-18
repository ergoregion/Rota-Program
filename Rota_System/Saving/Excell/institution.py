__author__ = 'Neil Butcher'

import xlwt



class PopulationSavingObject(object):
    '''
    classdocs
    '''

    def __init__(self, population, filename=None):
        if filename:
            self._filename = filename
        else:
            self._filename = institution.name + '.xls'

        self._population = population
        self._connection = sqlite3.connect(self._filename, detect_types=sqlite3.PARSE_DECLTYPES)

__author__ = 'Neil Butcher'


class ExcellImportExportError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Failure with import or export to excell ', self.value

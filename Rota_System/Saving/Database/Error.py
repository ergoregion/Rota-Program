__author__ = 'Neil Butcher'


class DatabaseSaveLoadError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Failure with saving/loading database ', self.value

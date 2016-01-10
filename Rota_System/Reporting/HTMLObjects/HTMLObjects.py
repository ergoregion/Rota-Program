__author__ = 'Neil Butcher'

from HTMLDisplay import display


class _HTMLObject(object):
    def __init__(self, *args):
        self.elements = []
        for arg in args:
            self.add(arg)

    def add(self, value):
        self.elements.append(value)

    def display(self):
        display(self)

    def extend(self, value):
        self.elements.extend(value)

    def attributes(self):
        return []

    def code(self):
        return ''

    def new_line(self):
        return False

    def html_string(self):
        s = '<'
        s += self.code()
        for a in self.attributes():
            s += ' '
            s += a
        s += '>'
        for value in self.elements:
            if isinstance(value, _HTMLObject):
                s += value.html_string()
            elif value is None:
                s += ''
            else:
                s += str(value)
        s += '</' + self.code() + '>'
        if self.new_line():
            s += '\n'
        return s


class HTMLTableCell(_HTMLObject):
    def __init__(self, *args):
        _HTMLObject.__init__(self, *args)
        self.elements = []
        self.span = [1, 1]
        if len(args) == 1:
            self.add(args[0])
        if len(args) == 3:
            self.add(args[0])
            self.span = args[1:]

    def code(self):
        return 'td'

    def attributes(self):
        if self.span == [1, 1]:
            return []
        else:
            return ['colspan=' + str(self.span[0]), 'rowspan=' + str(self.span[1])]


class HTMLNone(_HTMLObject):
    def html_string(self):
        return ''


class HTMLTableHeaderCell(HTMLTableCell):
    def code(self):
        return 'th'


class HTMLTableRow(_HTMLObject):
    def code(self):
        return 'tr'

    def new_line(self):
        return True


class HTMLTable(_HTMLObject):
    def code(self):
        return 'table'

    def new_line(self):
        return True

    def attributes(self):
        return ['border']


class HTMLParagraph(_HTMLObject):
    def code(self):
        return 'p'

    def new_line(self):
        return True


class HTMLAll(_HTMLObject):
    def code(self):
        return 'html'

    def new_line(self):
        return True


class HTMLListItem(_HTMLObject):
    def code(self):
        return 'li'


class HTMLTitle(_HTMLObject):
    def code(self):
        return 'h3'


class HTMLHeading(_HTMLObject):
    def code(self):
        return 'h1'


class HTMLGroup(_HTMLObject):
    def code(self):
        return 'span'


class HTMLHead(_HTMLObject):
    def code(self):
        return 'head'


class HTMLPageTitle(_HTMLObject):
    def code(self):
        return 'title'


class HTMLSuperscript(_HTMLObject):
    def code(self):
        return 'sup'


class HTMLSubscript(_HTMLObject):
    def code(self):
        return 'sub'


class HTMLList(_HTMLObject):
    def code(self):
        return 'ul'

    def new_line(self):
        return True

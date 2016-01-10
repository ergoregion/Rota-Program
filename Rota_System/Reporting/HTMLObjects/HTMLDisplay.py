__author__ = 'Neil Butcher'


from PyQt4.QtGui import QDialog, QVBoxLayout
from PyQt4.QtWebKit import QWebPage, QWebView

elements = {"like": "", "text": ""}


class MyWebPage(QWebPage):
    def acceptNavigationRequest(self, frame, req, nav_type):
        if nav_type == QWebPage.NavigationTypeFormSubmitted:
            text = "<br/>\n".join(["%s: %s" % pair for pair in req.url().queryItems()])
            print(text)
            return True
        else:
            return super(MyWebPage, self).acceptNavigationRequest(frame, req, nav_type)


class Window(QDialog):
    def __init__(self, html):
        super(Window, self).__init__()
        view = QWebView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(view)
        view.setPage(MyWebPage())
        view.setHtml(html.htmlString())


def display(html):

    window = Window(html)
    window.exec_()

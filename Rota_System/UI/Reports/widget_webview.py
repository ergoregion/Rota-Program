
from PyQt4 import QtWebKit


class WebView(QtWebKit.QWebView):
    def __init__(self, parent=None):
        super(WebView, self).__init__(parent)
        self.settings().setAttribute(QtWebKit.QWebSettings.JavascriptEnabled, True)

# pylint: skip-file

from unittest import mock

""" Mocks for PyScript """

class Element():
    def attr(self, name, value):
        return self

    def appendTo(self, other):
        return self

    def prependTo(self, other):
        return self

    def on(self, *args):
        return self

    def addClass(self, *args):
        return self

    def append(self, *args):
        return self

    def prepend(self, *args):
        return self

    def text(self, *args):
        return self

    def html(self, *args):
        return self

class Document():
    head = Element()
    body = Element()

class JavaScriptClass():
    def new(self):
        return 

class LocalStorage():
    def getItem(self, name):
        return "{}"

    def setItem(self, name, value):
        pass

class Window():
    localStorage = LocalStorage()
    document = Document()

    def parseInt(self, s):
        return int(s)

    def parseFloat(self, s):
        return float(s)
    
    def jQuery(self, *args):
        return Element()

    def Date(self, *args):
        return JavaScriptObject()

    def get_time(self):
        return 0

window = Window()
RUNNING_IN_WORKER = False
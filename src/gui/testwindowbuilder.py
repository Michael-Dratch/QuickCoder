from PyQt6.QtWidgets import QHBoxLayout
from src.gui.mainwindow import MainWindow
from src.gui.documentlistview import DocumentListView


class TestWindowBuilder:

    def build(self):
        window = MainWindow()
        window.x = 200
        window.y = 200
        window.w = 900
        window.h = 600
        window.setGeometry(window.x, window.y, window.w, window.h)
        window.setWindowTitle("QuickCode")
        self.initializeComponents(window)
        return window

    def initializeComponents(self, window):
        self.projectView = DocumentListView(self.printSelected, self.saveNewName, self.deleteDoc)
        layout = QHBoxLayout()
        layout.addWidget(self.projectView)
        window.setLayout(layout)

    def printSelected(self, doc):
        print(doc.name + 'selected')

    def saveNewName(self, doc, name):
        print(doc.name)
        print(name)

    def deleteDoc(self, doc):
        print(doc.name, 'deleted')

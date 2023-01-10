from PyQt6.QtWidgets import QHBoxLayout
from src.gui.mainwindow import MainWindow
from src.gui.codelistview import CodeListView


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
        self.codeListView = CodeListView(self.newCodeSelected, self.updateCode, self.deleteCode)
        layout = QHBoxLayout()
        layout.addWidget(self.codeListView)
        window.setLayout(layout)

    def newCodeSelected(self, doc):
        print(doc.name + 'selected')

    def updateCode(self, code, newName, newColor):
        print('updating')
        print(newName)
        print(newColor)

    def deleteCode(self, code):
        print(code.name, 'deleted')

from PyQt6.QtWidgets import QHBoxLayout

from src.datastructures import Code, CodeInstance
from src.gui.editor import Editor
from src.gui.mainwindow import MainWindow
from src.gui.codelistview import CodeListView


class TestWindowBuilder:

    def __init__(self, createCodeInstanceHandler):
        self.createCodeInstanceHandler = createCodeInstanceHandler

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
        self.editor = Editor(window, self.createCodeInstanceHandler)
        layout = QHBoxLayout()
        layout.addWidget(self.editor)
        window.setLayout(layout)



def createCodeInstance():
    instance1 = CodeInstance(1,
                            'd be form’d, till the ductile anchor hold, Till the gossamer thread you fling catch somewhere, O',
                            447, 543, Code(1, 'code1', '#FFAAAA'))
    instance2 = CodeInstance(2,
                             'sdlfisdj',
                             5, 10, Code(2, 'code2', "#AAAAEE"))
    return [instance1, instance2]
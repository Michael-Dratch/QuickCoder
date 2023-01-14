from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QDockWidget, QVBoxLayout

from src.gui.codelistview import CodeListView
from src.gui.documentlistview import DocumentListView
from src.gui.mainwindow import MainWindow
from src.gui.menubar import MenuBar
from src.gui.editor import Editor
# from src.gui.codeview import CodeView


class MainWindowBuilder:
    def __init__(self, controller):
        self.controller = controller
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
        menuBar = MenuBar(window)
        window.documentListView = DocumentListView(self.controller.changeSelectedDoc,
                                            self.controller.changeDocName,
                                            self.controller.deleteDoc)
        window.codeListView = CodeListView(self.controller.changeSelectedCode,
                                           self.controller.updateCode,
                                           self.controller.deleteCode)

        window.editor = Editor(window, self.controller.createCodeInstance, self.controller.saveCodeInstances)

        projectLayout = QVBoxLayout()
        projectLayout.addWidget(window.documentListView)
        projectLayout.addWidget(window.codeListView)
        # window.codeView = CodeView()
        innerLayout = QHBoxLayout()
        innerLayout.addLayout(projectLayout)
        innerLayout.addWidget(window.editor)
        # innerLayout.addWidget(window.codeView)
        outerLayout = QVBoxLayout()
        outerLayout.addWidget(menuBar)
        outerLayout.addLayout(innerLayout)
        window.setLayout(outerLayout)

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QTabWidget, QDockWidget, QVBoxLayout
from src.gui.mainwindow import MainWindow
from src.gui.menubar import MenuBar
from src.gui.editor import Editor
from src.gui.projectview import ProjectView
from src.gui.codeview import CodeView


class MainWindowBuilder:

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
        projectView = ProjectView()
        editor = Editor(window)
        codeView = CodeView()
        innerLayout = QHBoxLayout()
        innerLayout.addWidget(projectView)
        innerLayout.addWidget(editor)
        innerLayout.addWidget(codeView)
        outerLayout = QVBoxLayout()
        outerLayout.addWidget(menuBar)
        outerLayout.addLayout(innerLayout)
        window.setLayout(outerLayout)

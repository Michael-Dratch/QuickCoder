from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSplitter, QSizePolicy, QPushButton

from src.gui.codecomponents.codeinstancesview import CodeInstanceView
from src.gui.codecomponents.codelistview import CodeListView
from src.gui.documentcomponents.documentlistview import DocumentListView
from src.gui.documentcomponents.documentviewcontainer import DocumentViewContainer
from src.gui.gui import GUI
from src.gui.menubar import MenuBar
from src.gui.editor import Editor



class MainWindowBuilder:
    def __init__(self, controller):
        self.controller = controller

    def build(self):
        gui = GUI()
        gui.x = 200
        gui.y = 200
        gui.w = 1300
        gui.h = 800
        gui.setGeometry(gui.x, gui.y, gui.w, gui.h)
        gui.setWindowTitle("QuickCode")
        self.initializeComponents(gui)
        return gui

    def initializeComponents(self, gui):
        menuBar = MenuBar(gui, self.controller)
        gui.documentListView = DocumentListView(self.controller.changeSelectedDoc,
                                                self.controller.changeDocName,
                                                self.controller.deleteDoc)
        gui.codeListView = CodeListView(self.controller.changeSelectedCode,
                                        self.controller.updateCode,
                                        self.controller.deleteCode)

        gui.editor = Editor(gui, self.controller.createCodeInstance)

        gui.codeInstanceView = CodeInstanceView(self.controller.selectCodeInstance, self.controller.deleteCodeInstance)

        gui.documentViewContainer = DocumentViewContainer(gui.documentListView)

        codeWindow = QWidget()
        codeWindow.setMaximumWidth(400)
        codeLayout = QVBoxLayout()
        newCodeBtn = QPushButton('Create New Code')
        newCodeBtn.clicked.connect(self.controller.createCodeButtonHandler)
        codeLayout.addWidget(newCodeBtn)
        codeLayout.addWidget(QLabel('Project codes:'))
        codeLayout.addWidget(gui.codeListView)
        codeLayout.addWidget(QLabel('Code references:'))
        codeLayout.addWidget(QLabel('Sentiment       Text'))
        codeLayout.addWidget(gui.codeInstanceView)
        codeWindow.setLayout(codeLayout)



        innerLayout = QSplitter()
        innerLayout.addWidget(gui.documentViewContainer)
        innerLayout.addWidget(gui.editor)
        innerLayout.addWidget(codeWindow)
        innerLayout.setChildrenCollapsible(False)
        innerLayout.setSizes([200, 800, 300])
        innerLayout.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


        outerLayout = QVBoxLayout()
        outerLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        outerLayout.addWidget(menuBar)
        outerLayout.addWidget(innerLayout)
        gui.setLayout(outerLayout)

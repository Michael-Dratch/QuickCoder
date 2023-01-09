from functools import partial

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMenu
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from docselectbutton import DocSelectButton


class ProjectView(QWidget):

    def __init__(self, docSelectedHandler, saveDocNameHandler):
        super().__init__()
        self.docSelectedHandler = docSelectedHandler
        self.saveDocNameHandler = saveDocNameHandler
        self.setGeometry(0, 0, 100, 600)
        projectHeader = QLabel("Project1")
        self.createLayout(projectHeader)
        self.currentDoc = None
        self.documents = []

    def createLayout(self, projectHeader):
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.docsLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(projectHeader)
        self.layout.addLayout(self.docsLayout)

    def setDocuments(self, documents):
        self.documents = documents

    def setCurrentDoc(self, document):
        self.currentDoc = document

    def createButtons(self):
        for doc in self.documents:
            button = DocSelectButton(doc, self, self.saveDocNameHandler)
            button.setStyleSheet('text-align: left')
            button.clicked.connect(partial(self.docSelectedHandler, button.doc))
            self.setButtonContextMenuPolicy(button)
            self.layout.addWidget(button)

    def setButtonContextMenuPolicy(self, button):
        button.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        button.customContextMenuRequested.connect(button.on_context_menu)


from functools import partial

from PyQt6 import QtGui
from PyQt6.QtWidgets import QPushButton, QMenu, QLineEdit, QWidget, QVBoxLayout


class DocSelectButton(QPushButton):
    def __init__(self, doc, parent, saveDocNameHandler):
        super().__init__(doc.name, parent)
        self.saveDocNameHandler = saveDocNameHandler
        self.nameField = None
        self.editPopUp = None
        self.doc = doc
        self.createContextMenu()

    def createContextMenu(self):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        self.popMenu.addAction(editAction)
        editAction.triggered.connect(self.handleEditName)

    def on_context_menu(self, point):
        print(self.doc.name)
        self.popMenu.exec(self.mapToGlobal(point))

    def handleEditName(self):
        self.createEditNamePopUp()
        self.editPopUp.show()

    def createEditNamePopUp(self):
        nameField = QLineEdit()
        nameField.setText(self.doc.name)
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveName, nameField))
        layout = QVBoxLayout()
        layout.addWidget(nameField)
        layout.addWidget(saveButton)
        self.editPopUp = QWidget()
        self.editPopUp.setLayout(layout)

    def saveName(self, nameField):
        text = nameField.text()
        if text == '':
            return
        self.saveDocNameHandler(self.doc, text)


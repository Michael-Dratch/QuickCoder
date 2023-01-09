from functools import partial

from PyQt6 import QtGui
from PyQt6.QtWidgets import QPushButton, QMenu, QLineEdit, QWidget, QVBoxLayout, QMessageBox, QLabel, QHBoxLayout


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
        deleteAction = QtGui.QAction('delete document', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(self.handleEditName)
        deleteAction.triggered.connect(self.show_popup)

    def on_context_menu(self, point):
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

    def createDeleteDocPopUp(self):
        msg = QLabel("""Are you sure wish to delete {}?""".format(self.doc.name))
        cancelButton = QPushButton('Cancel')
        cancelButton.clicked.connect(partial(self.cancelClicked))
        deleteButton = QPushButton('Delete')
        deleteButton.clicked.connect(partial(self.DeleteClicked, self.doc))
        buttons = QHBoxLayout()
        buttons.addWidget(cancelButton)
        buttons.addWidget(deleteButton)

        layout = QVBoxLayout()
        layout.addWidget(msg)
        layout.addLayout(buttons)

        self.deletePopUp = QWidget()
        self.deletePopUp.setLayout(layout)

    def handleDeleteDocument(self):
        self.createDeleteDocPopUp()
        self.deletePopUp.show()

    def cancelClicked(self):
        self.deletePopUp.close()
    def popup_clicked(self, i):
        print(i.text())

    def show_popup(self):
        print("popup handler")
        choice = QtGui.QMessageBox.question(self, 'Extract!',
                                            "Get into the chopper?",
                                            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        print("22222")
        if choice == QtGui.QMessageBox.Yes:
            print("Extracting Naaaaaaoooww!!!!")
        else:
            pass
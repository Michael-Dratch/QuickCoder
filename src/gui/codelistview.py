from functools import partial

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget, QListWidget, QMenu, QDialog, QDialogButtonBox, \
    QLineEdit
from colorpanel import ColorPanel


class CodeListView(QListWidget):
    def __init__(self, codeSelectedHandler, updateCodeHandler, deleteCodeHandler):
        super().__init__()
        self.currentDoc = None
        self.codeSelectedHandler = codeSelectedHandler
        self.updateCodeHandler = updateCodeHandler
        self.deleteCodeHandler = deleteCodeHandler
        self.setGeometry(0, 0, 100, 600)
        self.codes = []
        self.currentItemChanged.connect(self.itemClicked)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def itemClicked(self, item):
        code = self.getCodeByName(item.text())
        self.codeSelectedHandler(code)

    def setCodes(self, codes):
        self.codes = codes
        for code in self.codes:
            self.addItem(code.name)

    def setCurrentDoc(self, document):
        self.currentDoc = document

    def createContextMenu(self, codeName):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit code', self)
        deleteAction = QtGui.QAction('delete code', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, codeName))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, codeName))

    def on_context_menu(self, point):
        codeName = self.itemAt(point).text()
        self.createContextMenu(codeName)
        self.popMenu.exec(self.mapToGlobal(point))

    def showEditWindow(self, codeName):
        self.createEditWindow(codeName)
        self.editPopUp.show()

    def createEditWindow(self, codeName):
        code = self.getCodeByName(codeName)
        nameField = QLineEdit()
        nameField.setText(code.name)
        colorLabel = QLabel("""Color: {}""".format(code.color))
        changeColorButton = QPushButton('Change color')
        changeColorButton.clicked.connect(self.showColorDiolog)
        color = QColorDialog.getColor()
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveName, docName, nameField))
        layout = QVBoxLayout()
        layout.addWidget(nameField)
        layout.addWidget(saveButton)

        self.editPopUp = QWidget()
        self.editPopUp.setLayout(layout)

    def showColorDiolog(self, oldColor):
        colorDialog = QColorDi

    def saveName(self, docName, nameField):
        text = nameField.text()
        if text == '':
            return
        doc = self.getDocByName(docName)
        self.saveDocNameHandler(doc, text)
        self.editPopUp.close()

    def showDeleteDialog(self, codeName):
        dialog = DeleteCodeDialog(codeName)
        if dialog.exec():
            code = self.getCodeByName(codeName)
            self.deleteCodeHandler(code)
        else:
            pass

    def getCodeByName(self, codeName):
        for code in self.codes:
            if code.name == codeName:
                return code


class DeleteCodeDialog(QDialog):
    def __init__(self, codeName):
        super().__init__()
        self.setWindowTitle("Delete Code")
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete {}?\nThis will delete all instances of this code in project documents.""".format(codeName))
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

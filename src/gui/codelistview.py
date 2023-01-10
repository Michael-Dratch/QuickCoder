from functools import partial

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QDockWidget, QLabel, QVBoxLayout, QWidget, QListWidget, QMenu, QDialog, QDialogButtonBox, \
    QLineEdit, QListWidgetItem, QPushButton, QHBoxLayout, QColorDialog


class CodeListView(QListWidget):
    def __init__(self, codeSelectedHandler, updateCodeHandler, deleteCodeHandler):
        super().__init__()
        self.editWindow = None
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
            item = QListWidgetItem(code.name, self)
            icon = self.createColorIcon(code.color)
            item.setIcon(icon)
            self.addItem(item)

    def createColorIcon(self, color):
        pixMap = QPixmap(20, 20)
        pixMap.fill(QColor(color))
        icon = QIcon(pixMap)
        return icon

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
        code = self.getCodeByName(codeName)
        self.editWindow = EditCodeWindow(code, self.updateCodeHandler)
        self.editWindow.show()

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


class EditCodeWindow(QWidget):
    def __init__(self, code, updateCodeHandler):
        super().__init__()
        self.code = code
        self.colorSquareLabel = None
        self.name = code.name
        self.color = code.color
        self.updateCodeHandler = updateCodeHandler
        self.setUpEditForm(code)


    def setUpEditForm(self, code):
        nameLayout = self.createEditNameLayout(code)
        colorLayout = self.createEditColorLayout(code)
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveUpdatedCode, code))
        layout = QVBoxLayout()
        layout.addLayout(nameLayout)
        layout.addLayout(colorLayout)
        layout.addWidget(saveButton)
        self.setLayout(layout)

    def createEditNameLayout(self, code):
        nameLabel = QLabel('code name: ')
        self.nameField = QLineEdit()
        self.nameField.setText(code.name)
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameField)
        return nameLayout
    def createEditColorLayout(self, code):
        colorLabel = QLabel('Color: ')
        self.colorSquareLabel = self.createColorSquareWidget(code.color)
        changeColorButton = QPushButton('Change color')
        changeColorButton.clicked.connect(self.openColorDialog)
        self.colorLayout = QHBoxLayout()
        self.colorLayout.addWidget(colorLabel)
        self.colorLayout.addWidget(self.colorSquareLabel)
        self.colorLayout.addWidget(changeColorButton)
        return self.colorLayout

    def createColorSquareWidget(self, color):
        colorPixMap = self.createPixMap(color)
        colorSquareLabel = QLabel()
        colorSquareLabel.setPixmap(colorPixMap)
        return colorSquareLabel

    def openColorDialog(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.setColor(color.name())
            
    def setColor(self, color):
        self.colorLayout.removeWidget(self.colorSquareLabel)
        self.colorSquareLabel.setParent(None)
        self.colorSquareLabel = self.createColorSquareWidget(color)
        self.colorLayout.insertWidget(1, self.colorSquareLabel)
        self.color = color

    def createPixMap(self, color):
        pixMap = QPixmap(20, 20)
        pixMap.fill(QColor(color))
        return pixMap

    def saveUpdatedCode(self, code):
        newName = self.nameField.text()
        if newName == '':
            return
        self.updateCodeHandler(code, newName, self.color)
        self.close()

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

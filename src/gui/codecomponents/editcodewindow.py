from functools import partial

from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QColorDialog, QWidget


class EditCodeWindow(QWidget):
    def __init__(self, code, projectCodes, updateCodeHandler):
        super().__init__()
        self.code = code
        self.projectCodes = projectCodes
        self.colorSquareLabel = None
        self.name = code.name
        self.color = code.color
        self.updateCodeHandler = updateCodeHandler
        self.setUpEditForm(code)
        self.errorMessageShowing = False

    def setUpEditForm(self, code):
        nameLayout = self.createEditNameLayout(code)
        colorLayout = self.createEditColorLayout(code)
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveUpdatedCode, code))
        self.layout = QVBoxLayout()
        self.layout.addLayout(nameLayout)
        self.layout.addLayout(colorLayout)
        self.layout.addWidget(saveButton)
        self.setLayout(self.layout)

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
        if self.nameExists(newName):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Name already exists'))
                self.errorMessageShowing = True
        else:
            self.updateCodeHandler(code, newName, self.color)
            self.close()

    def nameExists(self, name):
        for code in self.projectCodes:
            if name == code.name:
                return True
        return False
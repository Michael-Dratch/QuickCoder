from functools import partial

from PyQt6.QtGui import QColor, QPixmap
from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QLineEdit, QHBoxLayout, QColorDialog, QWidget


class CreateCodeWindow(QWidget):
    def __init__(self, codes, createCodeHandler):
        super().__init__()
        self.codes = codes
        self.colorSquareLabel = None
        self.createCodeHandler = createCodeHandler
        self.errorMessageShowing = False
        self.setUpForm()

    def setUpForm(self):
        nameLayout = self.createNameLayout()
        colorLayout = self.createColorLayout()
        saveButton = QPushButton('save')
        saveButton.clicked.connect(self.saveNewCode)
        self.layout = QVBoxLayout()
        self.layout.addLayout(nameLayout)
        self.layout.addLayout(colorLayout)
        self.layout.addWidget(saveButton)
        self.setLayout(self.layout)

    def createNameLayout(self):
        nameLabel = QLabel('code name: ')
        self.nameField = QLineEdit()
        nameLayout = QHBoxLayout()
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameField)
        return nameLayout

    def createColorLayout(self):
        colorLabel = QLabel('Color: ')
        self.colorSquareLabel = self.createColorSquareWidget('#FFFFFF')
        self.color = '#FFFFFF'
        changeColorButton = QPushButton('Select color')
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

    def saveNewCode(self):
        name = self.nameField.text()
        if name == '':
            return
        if self.nameExists(name):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Name already exists'))
                self.errorMessageShowing = True
        else:
            self.createCodeHandler(name, self.color)
            self.close()

    def nameExists(self, name):
        for code in self.codes:
            if name == code.name:
                return True
        return False
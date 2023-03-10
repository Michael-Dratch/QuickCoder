from functools import partial

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QIcon
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidget, QMenu, QDialog, QDialogButtonBox, \
    QListWidgetItem, QPushButton

from src.gui.codecomponents.editcodewindow import EditCodeWindow


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
        self.itemClicked.connect(self.itemClickedHandler)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def itemClickedHandler(self, item):
        if item:
            code = self.getCodeByName(item.text())
            self.codeSelectedHandler(code)

    def setCodes(self, codes):
        self.codes = codes
        self.clear()
        for code in self.codes:
            self.addCodeToListView(code)

    def addCodeToListView(self, code):
        item = QListWidgetItem(code.name, self)
        icon = self.createColorIcon(code.color)
        item.setIcon(icon)
        self.addItem(item)
        return item

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
        item = codeName = self.itemAt(point)
        if item == None:
            return
        codeName = item.text()
        self.createContextMenu(codeName)
        self.popMenu.exec(self.mapToGlobal(point))

    def showEditWindow(self, codeName):
        code = self.getCodeByName(codeName)
        self.editWindow = EditCodeWindow(code, self.codes, self.updateCodeHandler)
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

    def addNewCode(self, code):
        self.codes.append(code)
        item = self.addCodeToListView(code)
        item.setSelected(True)

    def replaceUpdatedCode(self, oldCode, newCode):
        item = self.getItem(oldCode)
        item.setText(newCode.name)
        item.setIcon(self.createColorIcon(newCode.color))

    def getItem(self, code):
        for row in range(self.count()):
            item = self.item(row)
            if item.text() == code.name:
                return item

    def removeCode(self, code):
        item = self.getItem(code)
        itemIndex = self.row(item)
        self.takeItem(itemIndex)

class DeleteCodeDialog(QDialog):
    def __init__(self, codeName):
        super().__init__()
        self.setWindowTitle("Delete Code")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Cancel'), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(QPushButton('Delete'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete {}?\nThis will delete all instances of this code in project documents.""".format(codeName))
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction

class MenuBar(QMenuBar):
    def __init__(self, parent):
        super(MenuBar, self).__init__(parent)
        self.addMenus()

    def addMenus(self):
        self.addMenu(self.createFileMenu())
        self.addMenu(self.createEditMenu())
        self.addMenu(self.createHelpMenu())

    def createFileMenu(self):
        fileMenu = QMenu("File", self)
        #newAction = self.createAction("New", self.parent().newFile)
        # openAction = self.createAction("Open", self.parent().ioManager.openFile)
        # saveAction = self.createAction("Save", self.parent().ioManager.saveFile)
        # saveAsAction = self.createAction("Save As", self.parent().ioManager.saveAs)
        #closeAction = self.createAction("Close", self.parent().closeApp)
        #fileMenu.addActions([newAction, closeAction])
        return fileMenu

    def createEditMenu(self):
        editMenu = QMenu("Edit", self)
        return editMenu

    def createHelpMenu(self):
        helpMenu = QMenu("Help", self)
        return helpMenu




    def createAction(self, label, slot):
        action = QAction(self)
        action.setText(label)
        action.triggered.connect(slot)
        return action
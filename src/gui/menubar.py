from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction


class MenuBar(QMenuBar):
    def __init__(self, parent, controller):
        super(MenuBar, self).__init__(parent)
        self.controller = controller
        self.addMenus()

    def addMenus(self):
        self.addMenu(self.createFileMenu())
        self.addMenu(self.createEditMenu())

    def createFileMenu(self):
        fileMenu = QMenu("File", self)
        # newAction = self.createAction("New", self.parent().newFile)

        newDocumentAction = self.createAction("New Document", self.controller.createDocumentButtonHandler)
        newProjectAction = self.createAction("New Project", self.controller.showNewProjectWindow)
        loadAction = self.createAction("Open Project", self.controller.showLoadProjectWindow)
        saveAction = self.createAction("Save", self.controller.saveDocument)
        exitAction = self.createAction("Exit", self.controller.exit)
        fileMenu.addActions([newDocumentAction, newProjectAction, loadAction])
        fileMenu.addSeparator()
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        return fileMenu

    def createEditMenu(self):
        editMenu = QMenu("Edit", self)
        undoAction = self.createAction('Undo typing', self.controller.undoTyping)
        redoAction = self.createAction('Redo typing', self.controller.redoTyping)
        cutAction = self.createAction('Cut', self.controller.cutSelectedText)
        pasteAction = self.createAction('Paste', self.controller.paste)
        editMenu.addActions([undoAction, redoAction, cutAction, pasteAction])
        editMenu.addSeparator()
        codeAction = self.createAction('Code text  ctrl+H', self.controller.codeSelectedText)
        editMenu.addAction(codeAction)
        return editMenu

    def createAction(self, label, slot):
        action = QAction(self)
        action.setText(label)
        action.triggered.connect(slot)
        return action

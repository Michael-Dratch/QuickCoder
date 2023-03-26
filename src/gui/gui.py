from PyQt6.QtWidgets import *

from src.gui.codecomponents.createcodewindow import CreateCodeWindow
from src.gui.documentcomponents.createdocumentwindow import CreateDocumentWindow, CreateDocumentInFolderWindow


class GUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.documentTreeView = None
        self.documentViewContainer = None
        self.codeListView = None
        self.editor = None
        self.codeInstanceView = None

    def setDocumentTree(self, docTree):
        self.documentTreeView.setDocumentTree(docTree)

    def setCodes(self, codes):
        self.codeListView.setCodes(codes)

    def setCodeInstances(self, codeInstances):
        self.codeInstanceView.setCodeInstances(codeInstances)
        self.editor.setCodeInstances(codeInstances)
        self.editor.highlightAllCodeInstances()

    def setProject(self, project):
        self.documentViewContainer.setProject(project)

    def showCreateCodeWindow(self, codes, createNewCodeHandler):
        self.createCodeWindow = CreateCodeWindow(codes, createNewCodeHandler)
        self.createCodeWindow.show()

    def showCreateDocumentWindow(self, createDocHandler):
        self.newDocumentWindow = CreateDocumentInFolderWindow(self.documentTreeView.getRootItem(), self.documentTreeView.createNewDocHandler)
        self.newDocumentWindow.show()


    def addDocument(self, document):
        self.editor.setDisabled(False)
        self.setCurrentDoc(document)

    def setCurrentDoc(self, doc):
        self.editor.setDocument(doc)

    def removeDoc(self):
        self.editor.setText('Select or create document to start coding.')
        self.editor.setDisabled(True)

    def addNewCode(self, code):
        self.codeListView.addNewCode(code)

    def replaceUpdatedCode(self, oldCode, updatedCode):
        self.codeListView.replaceUpdatedCode(oldCode, updatedCode)
        self.editor.updateCodeInstanceColor(updatedCode)

    def removeCode(self, code):
        self.codeListView.removeCode(code)
        if self.editor.currentCode == code:
            self.editor.currentCode = None
    def setSelectedCode(self, code):
        self.editor.setCurrentCode(code)

    def setListedCodeInstances(self, codeInstances):
        self.codeInstanceView.setCodeInstances(codeInstances)

    def addCodeInstance(self, codeInstance):
        self.codeInstanceView.addCodeInstance(codeInstance)

    def codeSelectedText(self):
        self.editor.codeSelectedText()

    def selectCodeInstance(self, codeInstance):
        self.editor.setSelection(codeInstance.start, codeInstance.end)
        self.editor.setFocus()

    def removeCodeInstance(self, codeInstance):
        self.editor.removeCodeInstance(codeInstance)

    def getDocumentText(self):
        return self.editor.toPlainText()

    def insertDocument(self, parentItem, document):
        self.documentTreeView.insertDocument(parentItem, document.name, document.id)

    def undoTyping(self):
        self.editor.undo()

    def redoTyping(self):
        self.editor.redo()

    def cutSelectedText(self):
        self.editor.cut()

    def paste(self):
        self.editor.paste()


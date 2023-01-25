from PyQt6.QtWidgets import *

from src.gui.codecomponents.createcodewindow import CreateCodeWindow
from src.gui.documentcomponents.createdocumentwindow import CreateDocumentWindow


class GUI(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.documentListView = None
        self.documentViewContainer = None
        self.codeListView = None
        self.editor = None
        self.codeInstanceView = None

    def setDocuments(self, docs):
        self.documentListView.setDocuments(docs)

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

    def showCreateDocumentWindow(self, projectDocuments, createDocHandler):
        self.createDocumentWindow = CreateDocumentWindow(projectDocuments, createDocHandler)
        self.createDocumentWindow.show()

    def addDocument(self, document):
        self.documentListView.documents.append(document)
        self.documentListView.addItem(document.name)
        self.editor.setDisabled(False)
        self.setCurrentDoc(document)

    def setCurrentDoc(self, doc):
        self.documentListView.setCurrentDoc(doc)
        self.editor.setDocument(doc)

    def removeDoc(self, doc):
        self.documentListView.removeDoc(doc)
        if len(self.documentListView.documents) == 0:
            self.editor.setText('Create new document to start coding.')
            self.editor.setDisabled(True)

    def addNewCode(self, code):
        self.codeListView.addNewCode(code)

    def replaceUpdatedCode(self, oldCode, updatedCode):
        self.codeListView.replaceUpdatedCode(oldCode, updatedCode)
        self.editor.updateCodeInstanceColor(updatedCode)

    def removeCode(self, code):
        self.codeListView.removeCode(code)

    def setSelectedCode(self, code):
        self.editor.setCurrentCode(code)

    def setListedCodeInstances(self, codeInstances):
        self.codeInstanceView.setCodeInstances(codeInstances)

    def addCodeInstance(self, codeInstance):
        self.codeInstanceView.addCodeInstance(codeInstance)

    def selectCodeInstance(self, codeInstance):
        self.editor.setSelection(codeInstance.start, codeInstance.end)
        self.editor.setFocus()
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
        self.setCodeInstanceView = None

    def setDocuments(self, docs):
        self.documentListView.setDocuments(docs)

    def setCodes(self, codes):
        self.codeListView.setCodes(codes)

    def setCodeInstances(self, codeInstances):
        self.codeInstanceView.setCodeInstances(codeInstances)

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
        self.setCurrentDoc(document)

    def setCurrentDoc(self, doc):
        self.documentListView.setCurrentDoc(doc)
        self.editor.setDocument(doc)

    def removeDoc(self, doc):
        self.documentListView.removeDoc(doc)

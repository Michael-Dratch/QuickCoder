from PyQt6.QtWidgets import *

from src.gui.createcodewindow import CreateCodeWindow


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

    def setCurrentDoc(self, doc):
        self.documentListView.setCurrentDoc(doc)

    def setCodes(self, codes):
        self.codeListView.setCodes(codes)

    def setCodeInstances(self, codeInstances):
        self.codeInstanceView.setCodeInstances(codeInstances)

    def setProject(self, project):
        self.documentViewContainer.setProject(project)

    def showCreateCodeWindow(self, codes, createNewCodeHandler):
        self.createCodeWindow = CreateCodeWindow(codes, createNewCodeHandler)
        self.createCodeWindow.show()
from PyQt6.QtWidgets import *


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

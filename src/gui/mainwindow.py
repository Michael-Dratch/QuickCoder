from PyQt6.QtWidgets import *


class MainWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.documentListView = None
        self.codeListView = None
        self.editor = None

    def setDocuments(self, docs):
        self.documentListView.setDocuments(docs)

    def setCodes(self, codes):
        self.codeListView.setCodes(codes)
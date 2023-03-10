from functools import partial

from PyQt6.QtWidgets import QMenu, QListWidget

from PyQt6 import QtCore, QtGui

from src.gui.documentcomponents.deletedocumentdialog import DeleteDocumentDialog
from src.gui.documentcomponents.editdocnamewindow import EditDocNameWindow


class DocumentListView(QListWidget):

    def __init__(self, docSelectedHandler, saveDocNameHandler, deleteDocHandler):
        super().__init__()
        self.docSelectedHandler = docSelectedHandler
        self.saveDocNameHandler = saveDocNameHandler
        self.deleteDocHandler = deleteDocHandler
        self.setGeometry(0, 0, 100, 600)
        self.currentDoc = None
        self.documents = []
        self.currentItemChanged.connect(self.itemClicked)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)

    def itemClicked(self, item):
        if item:
            doc = self.getDocByName(item.text())
            self.docSelectedHandler(doc)

    def setDocuments(self, documents):
        self.documents = documents
        self.clear()
        for doc in self.documents:
            self.addItem(doc.name)

    def setCurrentDoc(self, document):
        self.currentDoc = document
        for row in range(self.count()):
            item = self.item(row)
            if item.text() == document.name:
                item.setSelected(True)
            else:
                item.setSelected(False)

    def removeDoc(self, doc):
        item = self.getItem(doc)
        row = self.row(item)
        self.takeItem(row)
        self.documents.remove(doc)
        if self.currentDoc == doc:
            if len(self.documents) != 0:
                self.setCurrentDoc(self.documents[0])

    def getDocByName(self, docName):
        for doc in self.documents:
            if doc.name == docName:
                return doc

    def getItem(self, doc):
        for row in range(self.count()):
            item = self.item(row)
            if item.text() == doc.name:
                return item

    def changeDocLabelHandler(self, doc, newName):
        item = self.getItem(doc)
        item.setText(newName)
        doc.name = newName

    def on_context_menu(self, point):
        item = self.itemAt(point)
        if item == None:
            return
        docName = item.text()
        self.createContextMenu(docName)
        self.popMenu.exec(self.mapToGlobal(point))

    def createContextMenu(self, docName):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete document', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, docName))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, docName))

    def showEditWindow(self, docName):
        doc = self.getDocByName(docName)
        self.editNameWindow = EditDocNameWindow(doc, self.documents, self.saveDocNameHandler,
                                                self.changeDocLabelHandler)
        self.editNameWindow.show()

    def showDeleteDialog(self, docName):
        dlg = DeleteDocumentDialog(docName)
        if dlg.exec():
            doc = self.getDocByName(docName)
            self.deleteDocHandler(doc)
        else:
            pass

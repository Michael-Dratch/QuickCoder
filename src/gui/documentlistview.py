from functools import partial

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMenu, QListWidget, QDialog, QDialogButtonBox, \
    QLineEdit

from PyQt6 import QtCore, QtGui


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
        doc = self.getDocByName(item.text())
        self.docSelectedHandler(doc)

    def setDocuments(self, documents):
        self.documents = documents
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
    def createContextMenu(self, docName):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete document', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, docName))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, docName))

    def on_context_menu(self, point):
        item = self.itemAt(point)
        if item == None:
            return
        docName = item.text()
        self.createContextMenu(docName)
        self.popMenu.exec(self.mapToGlobal(point))

    def showEditWindow(self, docName):
        doc = self.getDocByName(docName)
        self.editNameWindow = EditNameWindow(self.documents, doc, self.saveDocNameHandler)
        self.editNameWindow.show()


    def showDeleteDialog(self, docName):
        dlg = DeleteDocumentDialog(docName)
        if dlg.exec():
            doc = self.getDocByName(docName)
            self.deleteDocHandler(doc)
        else:
            pass

    def getDocByName(self, docName):
        for doc in self.documents:
            if doc.name == docName:
                return doc


class DeleteDocumentDialog(QDialog):
    def __init__(self, docName):
        super().__init__()
        self.setWindowTitle("Delete Document")
        self.docName = docName

        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Cancel'), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(QPushButton('Delete'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete {}?""".format(docName))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class EditNameWindow(QWidget):
    def __init__(self, projectDocs, doc, saveNameHandler):
        super().__init__()
        self.projectDocs = projectDocs
        self.saveNameHandler = saveNameHandler
        self.errorMessageShowing = False
        self.nameField = QLineEdit()
        self.nameField.setText(doc.name)
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveNameClicked, doc, self.nameField, self.saveNameHandler))
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nameField)
        self.layout.addWidget(saveButton)

        self.setLayout(self.layout)

    def saveNameClicked(self, doc, nameField, saveNameHandler):
        newName = nameField.text()
        if newName == '':
            return
        if self.docNameExists(newName):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Document name already exists'))
                self.errorMessageShowing = True
        else:
            saveNameHandler(doc, newName)
            self.close()

    def docNameExists(self, docName):
        for doc in self.projectDocs:
            if doc.name == docName:
                return True
        return False
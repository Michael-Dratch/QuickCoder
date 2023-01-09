from functools import partial

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMenu, QListWidget, QDialog, QDialogButtonBox, QLineEdit

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
        self.customContextMenuRequested.connect(partial(self.on_context_menu))

    def itemClicked(self, item):
        doc = self.getDocByName(item.text())
        self.docSelectedHandler(doc)


    def setDocuments(self, documents):
        self.documents = documents
        for doc in self.documents:
            self.addItem(doc.name)

    def setCurrentDoc(self, document):
        self.currentDoc = document


    def showOptions(self, item):
        self.options = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete document', self)
        self.options.addAction(editAction)
        self.options.addAction(deleteAction)
        editAction.triggered.connect(self.showEditWindow)
        deleteAction.triggered.connect(partial(self.showDeleteDialog, item))
        self.options.exec(self.mapToGlobal())

    def createContextMenu(self, docName):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete document', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, docName))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, docName))


    def on_context_menu(self, point):
        docName = self.itemAt(point).text()
        self.createContextMenu(docName)
        self.popMenu.exec(self.mapToGlobal(point))

    def showEditWindow(self, docName):
        self.createEditNameWindow(docName)
        self.editPopUp.show()


    def createEditNameWindow(self, docName):
        nameField = QLineEdit()
        nameField.setText(docName)
        saveButton = QPushButton('save')
        saveButton.clicked.connect(partial(self.saveName, docName, nameField))
        layout = QVBoxLayout()
        layout.addWidget(nameField)
        layout.addWidget(saveButton)

        self.editPopUp = QWidget()
        self.editPopUp.setLayout(layout)

    def saveName(self, docName, nameField):
        text = nameField.text()
        if text == '':
            return
        doc = self.getDocByName(docName)
        self.saveDocNameHandler(doc, text)
        self.editPopUp.close()


    def showDeleteDialog(self, docName):
        dlg = DeleteDocumentDialog(docName)
        print('creating object')
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
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete {}?""".format(docName))
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)



import ast
import os
from functools import partial

from PyQt6 import QtCore, QtGui
from PyQt6.QtWidgets import QTreeView, QMenu
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap

from src.gui.documentcomponents.createdocumentwindow import CreateDocumentInFolderWindow, CreateFolderInFolderWindow
from src.gui.documentcomponents.deletedocumentdialog import DeleteDocumentDialog
from src.gui.documentcomponents.editdocnamewindow import EditDocNameWindow, EditFolderNameWindow


def itemIsDocument(item):
    return item.data()[0] == 'DOCUMENT'


def itemIsFolder(item):
    return item.data()[0] == 'FOLDER'


class DocumentTreeView(QTreeView):
    def __init__(self, docSelectedHandler, saveDocNameHandler, deleteDocHandler, saveTreeData, createNewDocHandler):
        QTreeView.__init__(self)
        self.setMinimumWidth(300)
        self.setHeaderHidden(True)
        self.setTreeViewAttributes()
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.folderIcon = self.createFolderIcon()
        self.model.rowsRemoved.connect(self.rowRemovedHandler)
        self.treeData = {}
        self.clicked.connect(self.itemClicked)
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.docSelectedHandler = docSelectedHandler
        self.saveDocNameHandler = saveDocNameHandler
        self.deleteDocHandler = deleteDocHandler
        self.saveTreeData = saveTreeData
        self.createNewDocHandler = createNewDocHandler

    def setTreeViewAttributes(self):
        self.setSelectionMode(self.selectionMode().SingleSelection)
        self.setDragDropMode(self.dragDropMode().InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)

    def createFolderIcon(self):
        path = os.path.dirname(os.path.abspath(__file__))
        return QIcon(QPixmap(os.path.join(path, 'resources/folder.png')))

    def getRootItem(self):
        rootItem = self.model.invisibleRootItem()
        return rootItem

    def setData(self, data):
        parentItem = self.model.invisibleRootItem()
        self.setSubTree(data, parentItem)
        self.treeData = self.getTreeData()

    def setSubTree(self, data, parentItem):
        for key, value in data.items():
            if self.valueIsInteger(value):
                doc = self.createDocItem(key, value)
                parentItem.appendRow(doc)
            else:
                folder = self.createFolderItem(key)
                parentItem.appendRow(folder)
                self.setSubTree(value, folder)

    def valueIsInteger(self, value):
        return type(value) == int

    def addFolderIcon(self, item):
        item.setIcon(self.folderIcon)

    def createFolderItem(self, label):
        folder = QStandardItem(label)
        folder.setData(['FOLDER'])
        self.addFolderIcon(folder)
        return folder

    def createDocItem(self, label, docID):
        doc = QStandardItem(label)
        doc.setData(['DOCUMENT', docID])
        doc.setDropEnabled(False)
        return doc

    def insertDocument(self, parentItem, docName, docID):
        doc = self.createDocItem(docName, docID)
        parentItem.appendRow(doc)
        self.updateTreeData()
        self.saveTreeData(self.treeData)
        self.docSelectedHandler(docID)

    def updateTreeData(self):
        self.treeData = self.getTreeData()
        self.saveTreeData(self.treeData)

    def getTreeData(self):
        data = {}
        rootItem = self.model.invisibleRootItem()
        return self.getSubTreeData(rootItem, data)

    def getSubTreeData(self, rootItem, parentDictionary):
        for childIndex in range(rootItem.rowCount()):
            child = rootItem.child(childIndex)
            if child is not None:
                if itemIsFolder(child):
                    child_dictionary = {}
                    parentDictionary[child.text()] = self.getSubTreeData(child, child_dictionary)
                else:
                    parentDictionary[child.text()] = child.data()[1]
        return parentDictionary

    def itemClicked(self):
        currentIndex = self.currentIndex()
        item = self.model.itemFromIndex(currentIndex)
        if itemIsDocument(item):
            docID = item.data()[1]
            self.docSelectedHandler(docID)

    def printTree(self):
        rootItem = self.model.invisibleRootItem()
        self.printSubTree(rootItem, "")

    def printSubTree(self, rootItem, indent):
        for childIndex in range(rootItem.rowCount()):
            child = rootItem.child(childIndex)
            if child is not None:
                print(indent + child.data()[0] + ': ' + child.text())
                if child.hasChildren():
                    new_indent = indent + '\t'
                    self.printSubTree(child, new_indent)

    def rowRemovedHandler(self, parentIndex, childIndex):
        self.treeData = self.getTreeData()
        self.saveTreeData(self.treeData)

    def on_context_menu(self, point):
        index = self.indexAt(point)
        item = self.model.itemFromIndex(index)
        if item is None:
            return
        if itemIsDocument(item):
            docName = item.text()
            docID = item.data()[1]
            self.createDocumentContextMenu(item, docName, docID)
            self.popupMenu.exec(self.mapToGlobal(point))
        if itemIsFolder(item):
            folderName = item.text()
            self.createFolderContextMenu(item, folderName)
            self.popupMenu.exec(self.mapToGlobal(point))

    def createDocumentContextMenu(self, item, docName, docID):
        self.popupMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete document', self)
        self.popupMenu.addAction(editAction)
        self.popupMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, item, docName, docID))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, item, docName, docID))

    def showEditWindow(self, item, docName, docID):
        self.editNameWindow = EditDocNameWindow(item, docName, docID, self.saveDocNameHandler,
                                                self.changeItemLabelHandler)
        self.editNameWindow.show()

    def changeItemLabelHandler(self, item, newName):
        item.setText(newName)
        self.updateTreeData()

    def showDeleteDialog(self, item, docName, docID):
        dlg = DeleteDocumentDialog(docName)
        if dlg.exec():
            self.deleteDocument(item)
            self.updateTreeData()
            self.deleteDocHandler(docID)
        else:
            pass

    def createFolderContextMenu(self, item, name):
        self.popupMenu = QMenu(self)
        newDocumentAction = QtGui.QAction('new document', self)
        newFolderAction = QtGui.QAction('new folder', self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete folder', self)
        self.popupMenu.addAction(newDocumentAction)
        self.popupMenu.addAction(newFolderAction)
        self.popupMenu.addSeparator()
        self.popupMenu.addAction(editAction)
        self.popupMenu.addAction(deleteAction)
        newDocumentAction.triggered.connect(partial(self.showNewDocumentWindow, item))
        newFolderAction.triggered.connect(partial(self.showNewFolderWindow, item))
        editAction.triggered.connect(partial(self.showEditFolderWindow, item, name))
        deleteAction.triggered.connect(partial(self.showDeleteFolderDialog, item, name))

    def showNewDocumentWindow(self, item):
        self.newDocumentWindow = CreateDocumentInFolderWindow(item, self.createNewDocHandler)
        self.newDocumentWindow.show()

    def showNewFolderWindow(self, item):
        self.newFolderWindow = CreateFolderInFolderWindow(item, self.createNewFolderHandler)
        self.newFolderWindow.show()

    def createNewFolderHandler(self, parentItem, newName):
        parentItem.appendRow(self.createFolderItem(newName))
        self.updateTreeData()
        self.saveTreeData(self.treeData)

    def showEditFolderWindow(self, item, name):
        self.editFolderNameWindow = EditFolderNameWindow(item, name, self.changeItemLabelHandler)
        self.editFolderNameWindow.show()

    def showDeleteFolderDialog(self, item, folderName):
        dlg = DeleteDocumentDialog(folderName)
        if dlg.exec():
            self.deleteChildDocuments(item)
            self.model.takeRow(item.row())
            self.updateTreeData()
        else:
            pass

    def deleteChildDocuments(self, item):
        for childIndex in range(item.rowCount()):
            child = item.child(childIndex)
            if child is not None:
                if itemIsFolder(child):
                    self.deleteChildDocuments(child)
                else:
                    self.deleteDocHandler(child.data()[1])

    def deleteDocument(self, item):
        parent = item.parent()
        if parent is None:
            self.model.takeRow(item.row())
        else:
            parent.takeRow(item.row())

    def setDocumentTree(self, docTree):
        self.model.clear()
        print(len(docTree))
        if len(docTree) > 2:
            treeDict = ast.literal_eval(docTree)
            self.setData(treeDict)

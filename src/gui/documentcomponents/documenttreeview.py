import mimetypes
import os

from PyQt6 import QtCore
from PyQt6.QtWidgets import QTreeView
from PyQt6.QtGui import QStandardItemModel, QStandardItem, QIcon, QPixmap


class DocumentTreeView(QTreeView):
    def __init__(self):
        QTreeView.__init__(self)

        self.setSelectionMode(self.selectionMode().SingleSelection)
        self.setDragDropMode(self.dragDropMode().InternalMove)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        path = os.path.dirname(os.path.abspath(__file__))
        self.folderIcon = QIcon(QPixmap(os.path.join(path, 'resources/folder.png')))
        self.model.rowsRemoved.connect(self.rowRemovedHandler)
        self.treeData = {}

    def setData(self, data):
        parentItem = self.model.invisibleRootItem()
        self.setSubTree(data, parentItem)
        self.treeData = self.getTreeData()

    def setSubTree(self, data, parentItem):
        for key, value in data.items():
            if value is None:
                doc = self.createDocItem(key)
                parentItem.appendRow(doc)
            else:
                folder = self.createFolderItem(key)
                parentItem.appendRow(folder)
                self.setSubTree(value, folder)

    def addFolderIcon(self, item):
        item.setIcon(self.folderIcon)

    def createFolderItem(self, label):
        folder = QStandardItem(label)
        folder.setData('FOLDER')
        self.addFolderIcon(folder)
        return folder

    def createDocItem(self, label):
        doc = QStandardItem(label)
        doc.setData('DOCUMENT')
        doc.setDropEnabled(False)
        return doc

    def getTreeData(self):
        data = {}
        rootItem = self.model.invisibleRootItem()
        return self.getSubTreeData(rootItem, data)

    def getSubTreeData(self, rootItem, parentDictionary):
        for childIndex in range(rootItem.rowCount()):
            child = rootItem.child(childIndex)
            if child is not None:
                if child.data() == 'FOLDER':
                    child_dictionary = {}
                    parentDictionary[child.text()] = self.getSubTreeData(child, child_dictionary)
                else:
                    parentDictionary[child.text()] = None
        return parentDictionary

    def printTree(self):
        rootItem = self.model.invisibleRootItem()
        self.printSubTree(rootItem, "")

    def printSubTree(self, rootItem, indent):
        for childIndex in range(rootItem.rowCount()):
            child = rootItem.child(childIndex)
            if child is not None:
                print(indent + child.data() + ': ' + child.text())
                if child.hasChildren():
                    new_indent = indent + '\t'
                    self.printSubTree(child, new_indent)

    def rowRemovedHandler(self, parentIndex, childIndex):
        self.treeData = self.getTreeData()


from PyQt6.QtWidgets import QTreeView

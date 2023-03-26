from functools import partial
from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QToolButton, QFrame, QStackedLayout, \
    QMenu
from src.gui.documentcomponents.createdocumentwindow import CreateDocumentInFolderWindow, CreateFolderInFolderWindow


class DocumentViewContainer(QWidget):
    def __init__(self, documentTreeView, editProjectHandler):
        super().__init__()
        self.projectLabel = None
        self.editProjectHandler = editProjectHandler
        self.documentTreeView = documentTreeView
        self.layout = QStackedLayout()
        self.setLayout(self.layout)
        self.expandedDocView = self.buildExpandedLayout()
        self.collapsedDocView = self.buildCollapsedLayout()
        self.layout.addWidget(self.expandedDocView)
        self.layout.addWidget(self.collapsedDocView)
        self.setMaximumWidth(200)

    def buildExpandedLayout(self):
        expandedDocView = QFrame()
        documentViewLayout = QVBoxLayout()
        header = QHBoxLayout()
        self.projectLabel = QLabel()
        self.projectLabel.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.projectLabel.customContextMenuRequested.connect(self.onProjectContextMenu)
        header.addWidget(self.projectLabel)
        hideDocumentsButton = self.buildHideDocumentsButton()
        header.addWidget(hideDocumentsButton)
        documentViewLayout.addLayout(header)
        documentViewLayout.addWidget(self.documentTreeView)
        expandedDocView.setLayout(documentViewLayout)
        return expandedDocView

    def onProjectContextMenu(self, point):
        self.createProjectContextMenu()
        self.popupMenu.exec(self.mapToGlobal(point))

    def createProjectContextMenu(self):
        self.popupMenu = QMenu(self)
        newDocumentAction = QtGui.QAction('new document', self)
        newFolderAction = QtGui.QAction('new folder', self)
        editProjectAction = QtGui.QAction('edit project', self)
        self.popupMenu.addAction(newDocumentAction)
        self.popupMenu.addAction(newFolderAction)
        self.popupMenu.addSeparator()
        self.popupMenu.addAction(editProjectAction)
        newDocumentAction.triggered.connect(partial(self.showNewDocumentWindow))
        newFolderAction.triggered.connect(partial(self.showNewFolderWindow))
        editProjectAction.triggered.connect(partial(self.showEditProjectWindow))

    def showNewDocumentWindow(self):
        self.newDocumentWindow = CreateDocumentInFolderWindow(self.documentTreeView.getRootItem(),
                                                              self.documentTreeView.createNewDocHandler)
        self.newDocumentWindow.show()

    def showNewFolderWindow(self):
        self.newFolderWindow = CreateFolderInFolderWindow(self.documentTreeView.getRootItem(),
                                                          self.documentTreeView.createNewFolderHandler)
        self.newFolderWindow.show()

    def showEditProjectWindow(self):
        self.editProjectHandler()

    def buildCollapsedLayout(self):
        collapsedDocView = QFrame()
        collapsedLayout = QVBoxLayout()
        collapsedLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        expandButton = QToolButton()
        expandButton.setArrowType(QtCore.Qt.ArrowType.RightArrow)
        expandButton.setStyleSheet("""QToolButton { border: none; }
                                                   QToolButton:hover { 
                                                       background-color: darkgrey;}""")
        expandButton.clicked.connect(self.expandDocumentView)
        collapsedLayout.addWidget(expandButton)
        collapsedDocView.setLayout(collapsedLayout)
        return collapsedDocView

    def buildHideDocumentsButton(self):
        hideDocumentsButton = QToolButton()
        hideDocumentsButton.setArrowType(QtCore.Qt.ArrowType.LeftArrow)
        hideDocumentsButton.setStyleSheet("""QToolButton { border: none; }
                                            QToolButton:hover { 
                                                background-color: darkgrey;}""")
        hideDocumentsButton.clicked.connect(self.collapseDocumentView)
        return hideDocumentsButton

    def setProject(self, project):
        self.currentProject = project
        self.projectLabel.setText(project.name)

    def collapseDocumentView(self):
        self.expandedDocView.hide()
        self.collapsedDocView.show()
        self.setMaximumWidth(25)

    def expandDocumentView(self):
        self.collapsedDocView.hide()
        self.expandedDocView.show()
        self.setMaximumWidth(200)

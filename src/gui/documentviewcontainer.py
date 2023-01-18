from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QToolButton, QFrame, QStackedLayout


class DocumentViewContainer(QWidget):
    def __init__(self, documentListView):
        super().__init__()
        self.documentListView = documentListView
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
        header.addWidget(self.projectLabel)
        hideDocumentsButton = self.buildHideDocumentsButton()
        header.addWidget(hideDocumentsButton)
        documentViewLayout.addLayout(header)
        documentViewLayout.addWidget(self.documentListView)
        expandedDocView.setLayout(documentViewLayout)
        return expandedDocView

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
        self.projectLabel.setText(project.name)

    def collapseDocumentView(self):
        self.expandedDocView.hide()
        self.collapsedDocView.show()
        self.setMaximumWidth(25)
    def expandDocumentView(self):
        self.collapsedDocView.hide()
        self.expandedDocView.show()
        self.setMaximumWidth(200)




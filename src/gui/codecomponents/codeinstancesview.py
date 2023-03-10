from functools import partial

from PyQt6 import QtGui, QtCore
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QMenu, QWidget, QPushButton, QLabel, QDialog, \
    QDialogButtonBox, QVBoxLayout

from src.datastructures import Sentiment
from src.gui.codecomponents.codeinstancelistitem import CodeInstanceListItem


class CodeInstanceView(QListWidget):
    def __init__(self, codeInstanceSelectedHandler, deleteCodeInstanceHandler):
        super().__init__()
        self.codeInstanceSelectedHandler = codeInstanceSelectedHandler
        self.deleteCodeInstanceHandler = deleteCodeInstanceHandler
        self.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.currentItemChanged.connect(self.itemClicked)

    def itemClicked(self):
        item = self.currentItem()
        if item:
            itemWidget = self.itemWidget(item)
            codeInstance = itemWidget.codeInstance
            self.codeInstanceSelectedHandler(codeInstance)

    def setCodeInstances(self, codeInstances):
        self.codeInstances = codeInstances
        self.clear()
        for i in self.codeInstances:
            item = self.createCodeInstanceItem(i)
            self.addItem(item)

    def addCodeInstance(self, codeInstance):
        self.codeInstances.append(codeInstance)
        item = self.createCodeInstanceItem(codeInstance)
        self.addItem(item)

    def createCodeInstanceItem(self, codeInstance):
        item_widget = CodeInstanceListItem(codeInstance, self.showSentimentOptions)
        item = QListWidgetItem(self)
        item.setSizeHint(item_widget.sizeHint())
        self.setItemWidget(item, item_widget)
        return item

    def on_context_menu(self, point):
        item = self.itemAt(point)
        if item == None:
            return
        itemWidget = self.itemWidget(item)
        codeInstance = itemWidget.codeInstance
        rowID = self.row(item)
        self.createContextMenu(codeInstance, rowID, itemWidget)
        self.popMenu.exec(self.mapToGlobal(point))

    def createContextMenu(self, codeInstance, rowID, itemWidget):
        self.popMenu = QMenu(self)
        deleteAction = QtGui.QAction('delete code reference', self)
        sentimentAction = QtGui.QAction('change sentiment', self)
        self.popMenu.addAction(deleteAction)
        self.popMenu.addAction(sentimentAction)
        deleteAction.triggered.connect(partial(self.showDeleteDialog, codeInstance, rowID))
        sentimentAction.triggered.connect(partial(self.showSentimentOptions, codeInstance, itemWidget))

    def showDeleteDialog(self, codeInstance, rowID):
        dlg = DeleteCodeInstanceDialog()
        if dlg.exec():
            self.deleteCodeInstanceHandler(codeInstance)
            self.takeItem(rowID)
        else:
            pass

    def showSentimentOptions(self, codeInstance, itemWidget):
        sentimentWindow = ChangeSentimentWindow(codeInstance, itemWidget)
        sentimentWindow.show()




class DeleteCodeInstanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Delete Code Reference")
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton(QPushButton('Cancel'), QDialogButtonBox.ButtonRole.RejectRole)
        self.buttonBox.addButton(QPushButton('Delete'), QDialogButtonBox.ButtonRole.AcceptRole)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""Are you sure you wish to delete this code reference?""")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)


class ChangeSentimentWindow(QWidget):
    def __init__(self, codeInstance, itemWidget):
        super().__init__()
        self.codeInstance = codeInstance
        layout = QVBoxLayout()
        positiveBtn = QPushButton('Positive')
        positiveBtn.setIcon(QIcon('../resources/positive-icon.png'))
        positiveBtn.clicked.connect(partial(self.sentimentSelected, Sentiment.POSITIVE, itemWidget))

        negativeBtn = QPushButton('Negative')
        negativeBtn.setIcon(QIcon('../resources/negative-icon.png'))
        negativeBtn.clicked.connect(partial(self.sentimentSelected, Sentiment.NEGATIVE, itemWidget))

        neutralBtn = QPushButton('Neutral')
        neutralBtn.setIcon(QIcon('../resources/neutral-icon.png'))
        neutralBtn.clicked.connect(partial(self.sentimentSelected, Sentiment.NEUTRAL, itemWidget))

        noneBtn = QPushButton('None')
        noneBtn.clicked.connect(partial(self.sentimentSelected, None, itemWidget))

        layout.addWidget(positiveBtn)
        layout.addWidget(negativeBtn)
        layout.addWidget(neutralBtn)
        layout.addWidget(noneBtn)
        self.setLayout(layout)

    def sentimentSelected(self, sentiment, itemWidget):
        self.codeInstance.sentiment = sentiment
        itemWidget.updateSentimentButton()
        self.close()

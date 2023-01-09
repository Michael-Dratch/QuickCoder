from src.datastructures import Document
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.testwindowbuilder import TestWindowBuilder


def getNewDocList():
    doc1 = Document(1, 'doc1')
    doc2 = Document(2, 'doc2')
    return [doc1, doc2]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    builder = TestWindowBuilder()
    GUI = builder.build()

    docs = getNewDocList()

    projectView = builder.projectView
    projectView.setDocuments(docs)
    projectView.setCurrentDoc(docs[0])
    projectView.createButtons()
    GUI.show()
    sys.exit(app.exec())



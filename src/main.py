import sys
from PyQt6.QtWidgets import QApplication

from src.datastructures import Document
from src.gui.mainwindowbuilder import MainWindowBuilder
from projectcontroller import ProjectController
from database.database import Database




def getNewDocList():
    doc1 = Document(1, 'doc1')
    doc2 = Document(2, 'doc2')
    return [doc1, doc2]

if __name__=="__main__":

    app = QApplication(sys.argv)
    projectController = ProjectController()
    builder = MainWindowBuilder(projectController)

    GUI = builder.build()
    database = Database()

    projectController.setGUI(GUI)
    projectController.setDatabase(database)

    GUI.setDocuments(getNewDocList())

    GUI.show()
    sys.exit(app.exec())
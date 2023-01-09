import sys
from PyQt6.QtWidgets import QApplication
from src.gui.mainwindowbuilder import MainWindowBuilder
from projectcontroller import ProjectController
from database.database import Database

if __name__=="__main__":

    app = QApplication(sys.argv)
    builder = MainWindowBuilder()
    GUI = builder.build()

    database = Database()

    projectController = ProjectController()
    projectController.setGUI(GUI)
    projectController.setDatabase(database)

    GUI.show()
    sys.exit(app.exec())


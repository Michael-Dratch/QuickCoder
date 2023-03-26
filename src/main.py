import sys
from PyQt6.QtWidgets import QApplication
from src.gui.mainwindowbuilder import MainWindowBuilder
from projectcontroller import ProjectController
from database.database import Database
from src.gui.projectcomponents.projectview import ProjectView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    projectController = ProjectController()

    builder = MainWindowBuilder(projectController)
    GUI = builder.build()
    database = Database()
    database.initializeDatabase(':memory:')
    database.initializeTables()
    projectController.setGUI(GUI)
    projectController.setDatabase(database)

    projectView = ProjectView(None,
                  projectController.database.getProjects(),
                  projectController.createNewProject,
                  projectController.loadProject,
                  projectController.showGUI,
                  projectController.saveProjectName,
                  projectController.deleteProject)

    projectController.createNewTestProject('project') #LOAD DATA

    projectController.setProjectView(projectView)
    projectController.start()
    sys.exit(app.exec())

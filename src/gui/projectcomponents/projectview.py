from functools import partial

from PyQt6 import QtCore, QtGui
from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout, QMenu

from src.gui.projectcomponents.createprojectwindow import CreateProjectWindow
from src.gui.projectcomponents.deleteprojectdialog import DeleteProjectDialog
from src.gui.projectcomponents.projectwindow import EditProjectNameWindow


class ProjectViewBase(QWidget):
    def __init__(self, currentProject, projects, loadProjectHandler, saveProjectNameHandler, deleteProjectHandler):
        super().__init__()
        self.currentProject = currentProject
        self.projects = projects
        self.loadProjectHandler = loadProjectHandler
        self.saveProjectNameHandler = saveProjectNameHandler
        self.deleteProjectHandler = deleteProjectHandler

    def buildWindow(self):
        self.layout = QVBoxLayout()
        self.layout.addWidget(QLabel('Load Project:'))
        self.projectList = QListWidget()
        self.projectList.itemClicked.connect(self.itemClickedHandler)
        self.projectList.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.projectList.customContextMenuRequested.connect(self.on_context_menu)
        for project in self.projects:
            self.projectList.addItem(project.name)
        self.layout.addWidget(self.projectList)
        self.setLayout(self.layout)

    def itemClickedHandler(self):
        item = self.projectList.selectedItems()[0]
        project = self.getProjectByName(item.text())
        self.loadProjectHandler(project)
        self.close()

    def getProjectByName(self, name):
        for project in self.projects:
            if project.name == name:
                return project

    def getItem(self, project):
        for row in range(self.projectList.count()):
            item = self.projectList.item(row)
            if item.text() == project.name:
                return item

    def changeProjectLabelHandler(self, project, newName):
        item = self.getItem(project)
        item.setText(newName)
        project.name = newName

    def deleteProjectLabelHandler(self, project):
        item = self.getItem(project)
        row = self.projectList.row(item)
        self.projectList.takeItem(row)

    def on_context_menu(self, point):
        item = self.projectList.itemAt(point)
        if item == None:
            return
        projectName = item.text()
        self.createContextMenu(projectName)
        self.popMenu.exec(self.mapToGlobal(point))

    def createContextMenu(self, projectName):
        self.popMenu = QMenu(self)
        editAction = QtGui.QAction('edit name', self)
        deleteAction = QtGui.QAction('delete project', self)
        self.popMenu.addAction(editAction)
        self.popMenu.addAction(deleteAction)
        editAction.triggered.connect(partial(self.showEditWindow, projectName))
        deleteAction.triggered.connect(partial(self.showDeleteDialog, projectName))

    def showEditWindow(self, projectName):
        project = self.getProjectByName(projectName)
        self.editNameWindow = EditProjectNameWindow(project, self.projects, self.saveProjectNameHandler,
                                                    self.changeProjectLabelHandler)
        self.editNameWindow.show()

    def showDeleteDialog(self, projectName):
        dlg = DeleteProjectDialog(projectName)
        if dlg.exec():
            project = self.getProjectByName(projectName)
            self.deleteProjectHandler(project)
            self.deleteProjectLabelHandler(project)
            if project.id == self.currentProject.id:
                self.close()
        else:
            pass


class LoadProjectView(ProjectViewBase):
    def __init__(self, currentProject, projects, loadProjectHandler, saveProjectNameHandler, deleteProjectHandler):
        super().__init__(currentProject, projects, loadProjectHandler, saveProjectNameHandler, deleteProjectHandler)
        self.setWindowTitle('Load Project')
        self.buildWindow()


class ProjectView(ProjectViewBase):
    def __init__(self, currentProject,  projects, newProjectHandler, loadProjectHandler, showGUI, saveProjectNameHandler, deleteProjectHandler):
        super().__init__(currentProject, projects, loadProjectHandler, saveProjectNameHandler, deleteProjectHandler)
        self.setWindowTitle('QuickCode')
        self.newProjectHandler = newProjectHandler
        self.showGUI = showGUI
        self.buildWindow()
        self.addProjectBtn()

    def addProjectBtn(self):
        newProjectBtn = QPushButton('Create New Project')
        newProjectBtn.clicked.connect(self.getNewProjectName)
        self.layout.insertWidget(0, newProjectBtn)

    def getNewProjectName(self):
        self.createProjectWindow = CreateProjectWindow(self.projects, self.newProjectHandler, self.closeProjectView)
        self.createProjectWindow.show()

    def closeProjectView(self):
        self.showGUI()
        self.close()

    def itemClickedHandler(self):
        item = self.projectList.selectedItems()[0]
        project = self.getProjectByName(item.text())
        self.loadProjectHandler(project)
        self.showGUI()
        self.close()


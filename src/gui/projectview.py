from PyQt6.QtCore import QAbstractListModel
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QLabel, QLineEdit, QHBoxLayout


class ProjectView(QWidget):
    def __init__(self, projects, newProjectHandler, loadProjectHandler):
        super().__init__()
        self.setWindowTitle('QuickCode')
        self.projects = projects
        self.newProjectHandler = newProjectHandler
        self.loadProjectHandler = loadProjectHandler
        self.buildWindow()

    def buildWindow(self):
        layout = QVBoxLayout()
        newProjectBtn = QPushButton('Create New Project')
        newProjectBtn.clicked.connect(self.getNewProjectName)
        layout.addWidget(newProjectBtn)
        layout.addWidget(QLabel('Load Project:'))
        projectList = QListWidget()
        projectList.currentItemChanged.connect(self.itemClicked)
        for project in self.projects:
            projectList.addItem(project.name)
        layout.addWidget(projectList)
        self.setLayout(layout)

    def getNewProjectName(self):
        self.createProjectWindow = CreateProjectWindow(self.projects, self.newProjectHandler)
        self.createProjectWindow.show()

    def itemClicked(self, item):
        project = self.getProjectByName(item.text())
        self.loadProjectHandler(project)

    def getProjectByName(self, name):
        for project in self.projects:
            if project.name == name:
                return project


class CreateProjectWindow(QWidget):
    def __init__(self, projects, newProjectHandler):
        super().__init__()
        self.projects = projects
        self.newProjectHandler = newProjectHandler
        self.errorMessageShowing = False
        self.setWindowTitle('New Project')
        self.layout = QVBoxLayout()
        nameLayout = QHBoxLayout()
        nameLabel = QLabel('Project Name:')
        self.nameField = QLineEdit()
        self.nameField.setMaxLength(50)
        nameLayout.addWidget(nameLabel)
        nameLayout.addWidget(self.nameField)
        createBtn = QPushButton('Create Project')
        createBtn.clicked.connect(self.createProjectClicked)
        self.layout.addLayout(nameLayout)
        self.layout.addWidget(createBtn)
        self.setLayout(self.layout)

    def createProjectClicked(self):
        name = self.nameField.text()
        if name == "":
            return
        if self.nameExists(name):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Name already exists'))
                self.errorMessageShowing = True
        else:
            self.newProjectHandler(name)
            self.close()

    def nameExists(self, name):
        for project in self.projects:
            if name == project.name:
                return True
        return False

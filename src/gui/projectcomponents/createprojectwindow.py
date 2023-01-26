from PyQt6.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QVBoxLayout, QWidget


class CreateProjectWindow(QWidget):
    def __init__(self, projects, newProjectHandler, closeProjectView):
        super().__init__()
        self.projects = projects
        self.newProjectHandler = newProjectHandler
        self.closeProjectView = closeProjectView
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
            self.closeProjectView()
            self.close()

    def nameExists(self, name):
        for project in self.projects:
            if name == project.name:
                return True
        return False

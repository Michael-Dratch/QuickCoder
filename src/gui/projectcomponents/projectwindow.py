from functools import partial

from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QLabel


class ProjectWindowBase(QWidget):
    def __init__(self):
        super().__init__()
        self.errorMessageShowing = False
        self.nameField = QLineEdit()
        self.saveButton = QPushButton('save')
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.nameField)
        self.layout.addWidget(self.saveButton)
        self.setLayout(self.layout)

    def nameExists(self, name, projects):
        for project in projects:
            if project.name == name:
                return True
        return False


class EditProjectNameWindow(ProjectWindowBase):
    def __init__(self, project, projects, saveNameHandler):
        super().__init__()
        self.nameField.setText(project.name)
        self.setWindowTitle('Change Document Name')
        self.saveButton.clicked.connect(partial(self.saveNameClicked,
                                                project,
                                                projects,
                                                saveNameHandler))

    def saveNameClicked(self, project, projects, saveNameHandler):
        newName = self.nameField.text()
        if newName == '':
            return
        if self.nameExists(newName, projects):
            if not self.errorMessageShowing:
                self.layout.insertWidget(1, QLabel('Project name already exists'))
                self.errorMessageShowing = True
        else:
            saveNameHandler(project, newName)
            self.close()
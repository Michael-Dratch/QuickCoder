from src.gui.exitdialog import ExitDialog
from src.gui.projectcomponents.projectview import CreateProjectWindow, LoadProjectView, ProjectView


class ProjectController:
    def __init__(self):
        self.GUI = None
        self.projectView = None
        self.database = None
        self.currentProject = None
        self.currentDoc = None
        self.currentCode = None
        self.projectCodes = None
        self.projectDocs = None

    def start(self):
        self.projectView.show()

    def setGUI(self, gui):
        self.GUI = gui

    def setDatabase(self, database):
        self.database = database

    def setProjectView(self, projectView):
        self.projectView = projectView

    def createNewTestProject(self, name):
        self.currentProject = self.database.createProject(name)
        self.GUI.setProject(self.currentProject)
        self.currentDoc = self.database.createDocument('New Document', self.currentProject.id)
        self.projectDocs = [self.currentDoc]
        self.GUI.setDocuments(self.projectDocs)
        self.GUI.setCurrentDoc(self.currentDoc)
        self.currentCode = self.database.createCode('code1', '#00FF00', self.currentProject.id)
        self.projectCodes = [self.currentCode]
        self.GUI.setCodes(self.projectCodes)
        self.GUI.setSelectedCode(self.currentCode)
        self.GUI.editor.setText(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        self.GUI.setCodeInstances([])
        self.GUI.show()
        self.projectView.close()

    def showNewProjectWindow(self):
        projects = self.database.getProjects()
        self.createProjectWindow = CreateProjectWindow(projects, self.createNewProject, self.closeCreateProjectWindow)
        self.createProjectWindow.show()

    def closeCreateProjectWindow(self):
        self.createProjectWindow.close()

    def showGUI(self):
        self.GUI.show()

    def createNewProject(self, name):
        self.saveDocument()
        self.currentProject = self.database.createProject(name)
        self.GUI.setProject(self.currentProject)
        self.currentDoc = self.database.createDocument('New Document', self.currentProject.id)
        self.projectDocs = [self.currentDoc]
        self.GUI.setDocuments(self.projectDocs)
        self.GUI.setCurrentDoc(self.currentDoc)
        self.projectCodes = []
        self.GUI.setCodes(self.projectCodes)
        self.GUI.setCodeInstances([])

    def loadProject(self, project):
        self.saveDocument()
        self.currentProject = project
        self.GUI.setProject(project)
        self.loadDocuments(project)
        self.loadCodes(project)
        self.loadCodeInstances(project)

    def loadDocuments(self, project):
        self.projectDocs = self.database.getProjectDocuments(project.id)
        self.GUI.setDocuments(self.projectDocs)
        self.currentDoc = self.projectDocs[0]
        self.GUI.setCurrentDoc(self.currentDoc)

    def loadCodes(self, project):
        self.projectCodes = self.database.getProjectCodes(project.id)
        self.GUI.setCodes(self.projectCodes)
        self.currentCode = None

    def loadCodeInstances(self, project):
        codeInstances = self.database.getProjectCodeInstances(project.id)
        self.GUI.setCodeInstances(codeInstances)

    def showLoadProjectWindow(self):
        projects = self.database.getProjects()
        self.loadProjectWindow = LoadProjectView(self.currentProject,
                                                 projects,
                                                 self.loadProject,
                                                 self.saveProjectName,
                                                 self.deleteProject)
        self.loadProjectWindow.show()

    def saveProjectName(self, project, newName):
        self.database.updateProject(project.id, newName)
        if project.id == self.currentProject.id:
            self.GUI.setProject(project)

    def deleteProject(self, project):
        self.database.deleteProject(project.id)
        if self.currentProject.id == project.id:
            projects = self.database.getProjects()
            self.projectView = ProjectView(self.currentProject,
                                           projects,
                                           self.createNewProject,
                                           self.loadProject,
                                           self.showGUI,
                                           self.saveProjectName,
                                           self.deleteProject)
            self.projectView.show()
            self.GUI.close()

    def changeDocName(self, doc, newName):
        self.database.updateDocumentName(doc.id, newName, self.currentProject.id)

    def deleteDoc(self, doc):
        self.database.deleteDocument(doc.id)
        self.GUI.removeDoc(doc)

    def changeSelectedCode(self, code):
        self.currentCode = code
        self.GUI.setSelectedCode(code)
        filteredInstances = self.database.getDocumentCodeInstancesByCode(self.currentDoc.id, self.currentCode.id)
        self.GUI.setListedCodeInstances(filteredInstances)

    def updateCode(self, code, newName, color):
        self.database.updateCode(code.id, newName, color)
        updatedCode = self.database.getCode(code.id)
        self.GUI.replaceUpdatedCode(code, updatedCode)
        self.projectCodes.remove(code)
        self.projectCodes.append(updatedCode)

    def deleteCode(self, code):
        self.database.deleteCode(code.id)
        self.database.deleteAllInstancesOfCode(code.id)
        updatedInstances = self.database.getProjectCodeInstances(self.currentProject.id)
        self.GUI.removeCode(code)
        self.GUI.setCodeInstances(updatedInstances)
        if self.currentCode == code:
            self.currentCode = None
        self.projectCodes.remove(code)

    def codeSelectedText(self):
        self.GUI.codeSelectedText()

    def createCodeInstance(self, start, end, text):
        codeInstance = self.database.createCodeInstance(self.currentDoc,
                                                        self.currentCode,
                                                        text,
                                                        start,
                                                        end,
                                                        None)
        self.GUI.addCodeInstance(codeInstance)

    def exit(self):
        dlg = ExitDialog()
        if dlg.exec():
            self.GUI.close()
        else:
            pass

    def undoTyping(self):
        self.GUI.undoTyping()

    def redoTyping(self):
        self.GUI.redoTyping()

    def cutSelectedText(self):
        self.GUI.cutSelectedText()

    def paste(self):
        self.GUI.paste()

    def createCodeButtonHandler(self):
        self.GUI.showCreateCodeWindow(self.projectCodes, self.createNewCode)

    def createNewCode(self, name, color):
        code = self.database.createCode(name, color, self.currentProject.id)
        self.currentCode = code
        self.GUI.addNewCode(code)
        self.GUI.setSelectedCode(code)
        self.GUI.setListedCodeInstances([])

    def createDocumentButtonHandler(self):
        self.GUI.showCreateDocumentWindow(self.projectDocs, self.createNewDocument)

    def createNewDocument(self, name):
        self.saveDocument()
        document = self.database.createDocument(name, self.currentProject.id)
        self.currentDoc = document
        self.GUI.addDocument(self.currentDoc)
        self.GUI.setCodeInstances([])

    def saveDocument(self):
        if self.currentDoc:
            text = self.GUI.getDocumentText()
            self.database.updateDocumentText(self.currentDoc.id, text)

    def changeSelectedDoc(self, selectedDoc):
        self.saveDocument()
        document = self.database.getDocumentByID(selectedDoc.id)
        self.currentDoc = document
        self.GUI.setCurrentDoc(self.currentDoc)
        documentCodeInstances = self.database.getDocumentCodeInstances(self.currentDoc.id)
        self.GUI.setCodeInstances(documentCodeInstances)
        if self.currentCode:
            filteredInstances = self.database.getDocumentCodeInstancesByCode(self.currentDoc.id, self.currentCode.id)
            self.GUI.setListedCodeInstances(filteredInstances)

    def selectCodeInstance(self, codeInstance):
        self.GUI.selectCodeInstance(codeInstance)

    def deleteCodeInstance(self, codeInstance):
        self.database.deleteCodeInstance(codeInstance.id)
        self.GUI.removeCodeInstance(codeInstance)

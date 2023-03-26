import json

from src.gui.exitdialog import ExitDialog
from src.gui.projectcomponents.projectview import CreateProjectWindow, LoadProjectView, ProjectView
from src.gui.projectcomponents.projectwindow import EditProjectNameWindow


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
        self.project2 = self.database.createProject('project2')
        self.proj2doc1 = self.database.createDocument('doc1proj2', 2)
        proj2Data = str({'doc1proj2': self.proj2doc1.id})
        self.database.saveDocumentTree(2, proj2Data)
        self.GUI.setProject(self.currentProject)
        self.currentDoc = self.database.createDocument('doc1', self.currentProject.id)
        self.database.createDocument('doc2', self.currentProject.id)
        self.database.updateDocumentText(2, "document 2 text")
        data = {'doc1': 1, 'doc2': 2, 'folder': {}}
        self.database.saveDocumentTree(1, str(data))
        self.GUI.setDocumentTree(str(data))
        self.GUI.setCurrentDoc(self.currentDoc)
        self.currentCode = self.database.createCode('code1', '#00FF00', self.currentProject.id)
        self.projectCodes = [self.currentCode]
        self.GUI.setCodes(self.projectCodes)
        self.GUI.setSelectedCode(self.currentCode)
        self.GUI.editor.setText(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')
        self.GUI.setCodeInstances([])
        self.GUI.show()
        #self.projectView.close()

    def showNewProjectWindow(self):
        projects = self.database.getProjects()
        self.createProjectWindow = CreateProjectWindow(projects, self.createNewProject, self.closeCreateProjectWindow)
        self.createProjectWindow.show()

    def showEditProjectWindow(self):
        self.editNameWindow = EditProjectNameWindow(self.currentProject, self.database.getProjects(),
                                                    self.saveProjectName)
        self.editNameWindow.show()

    def closeCreateProjectWindow(self):
        self.createProjectWindow.close()

    def showGUI(self):
        self.GUI.show()

    def createNewProject(self, name):
        self.saveDocument()
        self.currentProject = self.database.createProject(name)
        self.GUI.setProject(self.currentProject)
        self.currentDoc = self.database.createDocument('New Document', self.currentProject.id)
        newDocTree = json.dumps({'New Document': self.currentDoc.id})
        self.database.saveDocumentTree(self.currentProject.id, newDocTree)
        self.GUI.setDocumentTree(newDocTree)
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
        docTree = self.database.getDocumentTree(project.id)
        self.GUI.setDocumentTree(docTree)
        self.currentDoc = self.projectDocs[0]
        self.GUI.setCurrentDoc(self.currentDoc)

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
            project.name = newName
            self.GUI.setProject(project)

    def loadCodes(self, project):
        self.projectCodes = self.database.getProjectCodes(project.id)
        self.GUI.setCodes(self.projectCodes)
        self.currentCode = None

    def loadCodeInstances(self, project):
        codeInstances = self.database.getProjectCodeInstances(project.id)
        self.GUI.setCodeInstances(codeInstances)

    def undoTyping(self):
        self.GUI.undoTyping()

    def redoTyping(self):
        self.GUI.redoTyping()

    def cutSelectedText(self):
        self.GUI.cutSelectedText()

    def paste(self):
        self.GUI.paste()

    def exit(self):
        dlg = ExitDialog()
        if dlg.exec():
            self.GUI.close()
        else:
            pass

    ############  CODE METHODS  #################

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

    def createCodeButtonHandler(self):
        self.GUI.showCreateCodeWindow(self.projectCodes, self.createNewCode)

    def createNewCode(self, name, color):
        code = self.database.createCode(name, color, self.currentProject.id)
        self.currentCode = code
        self.GUI.addNewCode(code)
        self.GUI.setSelectedCode(code)
        self.GUI.setListedCodeInstances([])

    def selectCodeInstance(self, codeInstance):
        self.GUI.selectCodeInstance(codeInstance)

    def deleteCodeInstance(self, codeInstance):
        self.database.deleteCodeInstance(codeInstance.id)
        self.GUI.removeCodeInstance(codeInstance)

    ############  DOCUMENT METHODS  #################
    def createNewDocument(self, name):
        self.saveDocument()
        document = self.database.createDocument(name, self.currentProject.id)
        self.currentDoc = document
        self.GUI.addDocument(self.currentDoc)
        self.GUI.setCodeInstances([])

    def createDocumentButtonHandler(self):
        self.GUI.showCreateDocumentWindow(self.createNewDocument)

    def saveDocName(self, docID, newName):
        self.database.updateDocumentName(docID, newName, self.currentProject.id)

    def deleteDoc(self, docID):
        self.database.deleteDocument(docID)
        if self.currentDoc.id == docID:
            self.currentDoc = None
            self.GUI.removeDoc()

    def saveTreeData(self, treeData):
        treeDataJson = str(treeData)
        self.database.saveDocumentTree(self.currentProject.id, treeDataJson)

    def createNewDocFromTreeHandler(self, parentItem, docName):
        document = self.database.createDocument(docName, self.currentProject.id)
        self.GUI.insertDocument(parentItem, document)

    def saveDocument(self):
        if self.currentDoc:
            text = self.GUI.getDocumentText()
            self.database.updateDocumentText(self.currentDoc.id, text)

    def changeSelectedDoc(self, docID):
        self.saveDocument()
        selectedDoc = self.database.getDocumentByID(docID)
        self.currentDoc = selectedDoc
        self.GUI.setCurrentDoc(self.currentDoc)
        documentCodeInstances = self.database.getDocumentCodeInstances(self.currentDoc.id)
        self.GUI.setCodeInstances(documentCodeInstances)
        if self.currentCode:
            filteredInstances = self.database.getDocumentCodeInstancesByCode(self.currentDoc.id, self.currentCode.id)
            self.GUI.setListedCodeInstances(filteredInstances)

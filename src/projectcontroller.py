from src.datastructures import Project, Document, CodeInstance, Sentiment
from src.gui.exitdialog import ExitDialog
from src.gui.projectview import CreateProjectWindow


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
        project = self.database.createProject(name)
        self.currentProject = project
        self.GUI.setProject(self.currentProject)
        document = self.database.createDocument('New Document', self.currentProject.id)
        self.currentDoc = document
        code1 = self.database.createCode('code1', '#00FF00', self.currentProject.id)
        self.currentCode = code1
        self.projectCodes = [code1]
        self.GUI.setCodes(self.projectCodes)
        self.GUI.setSelectedCode(code1)
        self.projectDocs = [self.currentDoc]
        self.GUI.setDocuments(self.projectDocs)
        self.GUI.setCurrentDoc(self.currentDoc)
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

    def createNewProject(self, name):
        project = self.database.createProject(name)
        self.currentProject = project
        self.GUI.setProject(self.currentProject)
        document = self.database.createDocument('New Document', self.currentProject.id)
        self.currentDoc = document
        self.projectCodes = []
        self.GUI.setCodes(self.projectCodes)
        self.projectDocs = [self.currentDoc]
        self.GUI.setDocuments(self.projectDocs)
        self.GUI.setCurrentDoc(self.currentDoc)
        self.GUI.setCodeInstances([])

    def showProjectWindow(self):
        self.GUI.show()

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

    def loadProject(self, project):
        print('loading ' + project.name)

    def showLoadProjectWindow(self):
        print('showing load project window')

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

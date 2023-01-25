from src.datastructures import Project, Document, CodeInstance, Sentiment


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
        self.GUI.editor.setText('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.')

        self.GUI.setCodeInstances([])
        self.GUI.show()
        self.projectView.close()

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
        self.GUI.show()
        self.projectView.close()

    def changeDocName(self, doc, newName):
        self.database.updateDocument(doc.id, newName, self.currentProject.id)

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

    def saveCodeInstances(self, codeInstances):
        print('saving codes')

    def createCodeInstance(self, start, end, text):
        codeInstance = self.database.createCodeInstance(self.currentDoc,
                                                        self.currentCode,
                                                        text,
                                                        start,
                                                        end,
                                                        None)
        self.GUI.addCodeInstance(codeInstance)

    def createNewDocument(self):
        print('creating new document')

    def loadProject(self, project):
        print('loading ' + project.name)

    def showLoadProjectWindow(self):
        print('showing load project window')

    def saveDocument(self):
        print('saving document')

    def exit(self):
        print('exiting')

    def undoTyping(self):
        print('undo')

    def redoTyping(self):
        print('redo')

    def cutSelectedText(self):
        print('cut')

    def paste(self):
        print('paste')

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
        document = self.database.createDocument(name, self.currentProject.id)
        self.GUI.addDocument(document)

    def changeSelectedDoc(self, doc):
        self.GUI.setCurrentDoc(doc)

    def selectCodeInstance(self, codeInstance):
        self.GUI.selectCodeInstance(codeInstance)
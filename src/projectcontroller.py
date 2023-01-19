from src.datastructures import Project, Document


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
    def createNewProject(self, name):
        projectID = self.database.createProject(name)
        self.currentProject = Project(projectID, name)
        self.GUI.setProject(self.currentProject)
        document = self.database.createDocument('New Document', projectID)
        self.currentDoc = document
        self.projectCodes = []
        self.GUI.setCodes(self.projectCodes)
        self.projectDocs = [self.currentDoc]
        self.GUI.setDocuments(self.projectDocs)
        self.GUI.setCurrentDoc(self.currentDoc)
        self.GUI.show()
        self.projectView.close()


    def changeDocName(self, doc, newName):
        self.database.updateDocument(doc.id, newName, self.currentProject.id)



    def deleteDoc(self, doc):
        self.database.deleteDocument(doc.id)
        self.GUI.removeDoc(doc)

    def changeSelectedCode(self, code):
        print('selected code ' + code.name)

    def updateCode(self, code, newName, color):
        print('updated code name: ' + newName + ' color: ' + color)

    def deleteCode(self, code):
        print('deleting code: ' + code.name)

    def saveCodeInstances(self, codeInstances):
        print('saving codes')

    def createCodeInstance(self, start, end, text):
        print('creating code instance')
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
        print(name)
        print(color)

    def createDocumentButtonHandler(self):
        self.GUI.showCreateDocumentWindow(self.projectDocs, self.createNewDocument)

    def createNewDocument(self, name):
        document = self.database.createDocument(name, self.currentProject.id)
        self.GUI.addDocument(document)

    def changeSelectedDoc(self, doc):
        self.GUI.setCurrentDoc(doc)


class ProjectController:
    def __init__(self):
        self.GUI = None
        self.database = None
        self.currentProject = None
        self.currentDoc = None
        self.currentCode = None

    def setGUI(self, gui):
        self.GUI = gui

    def setDatabase(self, database):
        self.database = database

    def hideDocumentView(self):
        print('hiding documentView')

    def showDocumentView(self):
        print('showing document view')

    def changeDocName(self, doc, newName):
        print("changing doc name")

    def changeSelectedDoc(self, doc):
        print('current doc ' + doc.name)
    def deleteDoc(self, doc):
        print('deleting ' + doc.name)

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
    def createNewProject(self, name):

        print('creating new project: ' + name)

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


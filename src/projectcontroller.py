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

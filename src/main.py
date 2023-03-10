import sys
from PyQt6.QtWidgets import QApplication, QWidget, QTreeWidget, QTreeWidgetItem, QPushButton

from src.datastructures import Document, Code, CodeInstance, Sentiment, Project
from src.gui.documentcomponents.documenttreeview import DocumentTreeView
from src.gui.mainwindowbuilder import MainWindowBuilder
from projectcontroller import ProjectController
from database.database import Database
from src.gui.projectcomponents.projectview import ProjectView


# testing functions
def getNewDocList():
    doc1 = Document(1, 'doc1', "")
    doc2 = Document(2, 'doc2', "")
    return [doc1, doc2]


def getNewCodeList():
    code1 = Code(1, 'code1', '#00FF00')
    code2 = Code(2, 'code2', '#0000FF')
    return [code1, code2]


def getNewCodeInstances(code):
    codeInstance1 = CodeInstance(1, 'sdfkjsdkfjh', 5, 10, Sentiment.POSITIVE, code)
    codeInstance2 = CodeInstance(2, 'sdfkjsdsdflsdj  sldkfjsd kfjh', 20, 30, Sentiment.NEUTRAL, code)
    return [codeInstance1, codeInstance2]


def getNewProject():
    return Project(1, 'project1')


def getProjectList():
    project1 = Project(1, 'project1')
    project2 = Project(2, 'project2')
    project3 = Project(3, 'project3')
    project4 = Project(4, 'project4')
    project5 = Project(5, 'project5')
    project6 = Project(6, 'project6')
    project7 = Project(7, 'project7')
    project8 = Project(8, 'project8')
    project9 = Project(9, 'project9')
    return [project1, project2, project3, project4, project5, project6, project7, project8, project9]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    projectController = ProjectController()

    # projectView = ProjectView(None,
    #                           [],
    #                           projectController.createNewProject,
    #                           projectController.loadProject,
    #                           projectController.showGUI,
    #                           projectController.saveProjectName,
    #                           projectController.deleteProject)
    #
    # builder = MainWindowBuilder(projectController)
    # GUI = builder.build()
    # database = Database()
    # database.initializeDatabase(':memory:')
    # database.initializeTables()
    # projectController.setGUI(GUI)
    # projectController.setDatabase(database)
    # projectController.setProjectView(projectView)
    #
    # projectController.createNewTestProject('project')

    #QTree Widget development




    data = {
        'folder1': {},
        'folder2': {'doc1': 1},
        'folder3': {'folder4': {}},
        'folder5': {'folder6': {'doc2': 2}},
        'doc3': 3
    }

    """
    list of items 
    [doc,
    folder,
    folder,
    doc
    
    class Folder:
        docs = []
        
        Notes:
    
    """
    def saveDocName(docID, newName):
        print('saving name')
        print(docID)
        print(newName)

    def deleteDoc(docID):
        print('deleting doc')
        print(docID)

    def docSelectedHandler(docID):
        print('selected')
        print(docID)

    def saveTreeData(treeData):
        print('saving')
        print(treeData)

    testWindow = QWidget()
    tree = DocumentTreeView(docSelectedHandler, saveDocName, deleteDoc, saveTreeData)
    tree.setParent(testWindow)
    tree.setMinimumHeight(500)

    tree.setMinimumWidth(300)

    tree.setData(data)
    def printTreeAndModel():
        tree.printTree()
        data = tree.getTreeData()
        print('tree model data')
        print(data)



    printButton = QPushButton(testWindow)
    printButton.setText('Print Tree')
    printButton.clicked.connect(printTreeAndModel)

    testWindow.show()

    #projectController.start()
    sys.exit(app.exec())

import sys
import unittest

from PyQt6.QtWidgets import QApplication, QWidget

from datastructures import *
from src.database.database import Database
from src.gui.mainwindowbuilder import MainWindowBuilder
from src.gui.projectview import ProjectView
from src.projectcontroller import ProjectController


class TestController(unittest.TestCase):

    def getNewDocList(self):
        doc1 = Document(1, 'doc1', "")
        doc2 = Document(2, 'doc2', "")
        return [doc1, doc2]

    def getNewCodeList(self):
        code1 = Code(1, 'code1', '#00FF00')
        code2 = Code(2, 'code2', '#0000FF')
        return [code1, code2]

    def getNewCodeInstances(self, code):
        codeInstance1 = CodeInstance(1, 'sdfkjsdkfjh', 5, 10, Sentiment.POSITIVE, code)
        codeInstance2 = CodeInstance(2, 'sdfkjsdsdflsdj  sldkfjsd kfjh', 20, 30, Sentiment.NEUTRAL, code)
        return [codeInstance1, codeInstance2]

    def getNewProject(self):
        return Project(1, 'project1')

    def getProjectList(self):
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


    def saveNewDocument(self, docName, text):
        self.database.createDocument(docName, 1)
        docID = self.database.cursor.lastrowid
        doc = Document(docID, docName, text)
        return doc



    def setUp(self):
        self.app = QApplication(sys.argv)
        self.projectController = ProjectController()

        builder = MainWindowBuilder(self.projectController)
        self.GUI = builder.build()
        self.database = Database()
        self.database.initializeDatabase(':memory:')
        self.database.initializeTables()
        self.projectController.setGUI(self.GUI)
        self.projectController.setDatabase(self.database)
        self.database.createProject('project1')
        self.projectController.currentProject = Project(1, 'project1')

    def test_change_doc_name(self):
        doc = self.saveNewDocument('testDoc', '')

        self.projectController.changeDocName(doc, 'new_name')
        updatedDoc = self.database.getDocumentByID(doc.id)
        self.assertEqual(updatedDoc.name, 'new_name')

    def test_select_doc(self):
        doc2Text = 'doc2_text'
        doc1 = self.saveNewDocument('doc1', 'doc1_text')
        doc2 = self.saveNewDocument('doc2', doc2Text)
        self.GUI.setDocuments([doc1, doc2])
        self.GUI.setCurrentDoc(doc1)

        self.GUI.setCurrentDoc(doc2)
        self.assertEqual(doc2Text, self.GUI.editor.toPlainText())

    def test_create_doc(self):
        self.projectController.createNewDocument('doc')
        doc = self.database.getDocumentByID(1)
        self.assertEqual(doc.name, 'doc')

    def test_delete_doc(self):
        doc = self.saveNewDocument('doc', '')
        self.GUI.setDocuments([doc])
        self.projectController.deleteDoc(doc)
        docs = self.database.getProjectDocuments(1)
        self.assertEqual(0, len(docs))

if __name__ == "__main__":
    unittest.main()

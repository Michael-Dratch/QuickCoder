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


    def test_nothing(self):
        pass





if __name__ == "__main__":
    unittest.main()

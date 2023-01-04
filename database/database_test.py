import sqlite3
import unittest
from database import Database
from datastructures.code import Code
import os


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.db = Database()
        self.db.setConnection(self.conn)
        self.db.initializeTables()

    def tearDown(self):
        self.cursor.execute("""DELETE FROM code;""")
        self.conn.commit()
        self.db.closeConnection()

    def assertTableExists(self, name):
        listOfTables = self.cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name=?; """, (name,)).fetchall()
        self.assertEqual(len(listOfTables), 1)

    def assertFieldExists(self, tableName, fieldName):
        sql_table_description = self.cursor.execute('''SELECT sql FROM sqlite_schema Where name=?''',
                                                    (tableName,)).fetchone()
        self.assertTrue(str(sql_table_description).__contains__(fieldName))

    def codeExists(self, codeName):
        self.cursor.execute("""SELECT * FROM code WHERE name=:name""", {'name': codeName})
        data = self.cursor.fetchall()
        return len(data) == 1

    def projectExists(self, name):
        self.cursor.execute("""SELECT * FROM project WHERE name=:name""", {'name': name})
        data = self.cursor.fetchall()
        return len(data) == 1

    def getNumRows(self, tableName):
        self.cursor.execute("""SELECT * FROM {}""".format(tableName))
        data = self.cursor.fetchall()
        return len(data)

    def test_createCodeTable(self):
        self.assertTableExists("code")
        self.assertTableExists("document")
        self.assertTableExists("project")
        self.assertTableExists("codeinstance")

    def test_create_code(self):
        self.db.createProject('test_project')
        self.db.createCode('positive', '#00FF00', 1)
        self.assertTrue(self.codeExists('positive'))

    def test_create_duplicate_code_fails(self):
        self.db.createProject('project')
        self.db.createCode('code', 'blue', 1)
        with self.assertRaises(Exception):
            self.db.createCode('code', 'green', 1)

    def test_delete_code(self):
        self.db.createProject('test_project')
        self.db.createCode('positive', '#00FF00', 1)
        self.db.deleteCode(codeId=1)
        self.assertEqual(0, self.getNumRows('code'))

    def test_update_code_name(self):
        oldName = 'oldName'
        newName = 'newName'
        color = '#00FF00'
        projectId = 1
        self.db.createProject('test_project')
        self.db.createCode(oldName, color, projectId)
        self.db.updateCode(1, newName, color)
        self.assertTrue(self.codeExists(newName))

    def test_getProjectCodes_None_Exist(self):
        codes = self.db.getProjectCodes(1)
        self.assertEqual(len(codes), 0)

    def test_getProjectCodes_Two_Exist(self):
        self.db.createProject('test_project')
        self.db.createCode('code1', '#FFFFFF', 1)
        self.db.createCode('code2', '#FFFFFF', 1)
        codes = self.db.getProjectCodes(1)
        self.assertEqual(len(codes), 2)
        self.assertEqual(codes[0].name, 'code1')
        self.assertEqual(codes[1].name, 'code2')

    def test_foreign_key_constraints(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.createCode('name', 'blue', 2)

    def test_create_project(self):
        self.db.createProject('test_project')
        self.assertTrue(self.projectExists('test_project'))

    def test_creating_duplicate_project_fails(self):
        self.db.createProject('project')
        with self.assertRaises(Exception):
            self.db.createProject('project')

    def test_delete_non_existant_project(self):
        self.db.deleteProject('project')

    def test_delete_project(self):
        self.db.createProject('project')
        self.db.deleteProject('project')
        self.assertFalse(self.projectExists('project'))

    def test_update_non_existent_project_fails(self):
        self.db.updateProject('oldName', 'newName')

    def test_update_project_name(self):
        self.db.createProject('oldName')
        self.db.updateProject('oldName', 'newName')
        self.assertFalse(self.projectExists('oldName'))
        self.assertTrue(self.projectExists('newName'))


    def test_create_document(self):
        self.db.createProject('test_project')
        self.db.createDocument('doc', 1)
        self.assertTrue(self.documentExists('doc'))

    # def test_create_duplicate_document_fails(self):
    #     self.db.createProject('project')
    #     self.db.createCode('code', 'blue', 1)
    #     with self.assertRaises(Exception):
    #         self.db.createCode('code', 'green', 1)


if __name__ == '__main__':
    unittest.main()


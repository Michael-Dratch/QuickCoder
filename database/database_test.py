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

    def codeExists(self, id, codeName, color, projectId):
        self.cursor.execute("""SELECT * FROM code""")
        data = self.cursor.fetchone()
        return str(data) == """({}, '{}', '{}', {})""".format(id, codeName, color, projectId)

    def getNumRows(self, tableName):
        self.cursor.execute("""SELECT * FROM {}""".format(tableName))
        data = self.cursor.fetchall()
        return len(data)

    def test_createCodeTable(self):
        self.assertTableExists("code")
        self.assertTableExists("document")
        self.assertTableExists("project")
        self.assertTableExists("codeinstance")

    def test_save_code(self):
        self.db.saveCode('positive', '#00FF00', 1)
        self.assertTrue(self.codeExists(1, 'positive', '#00FF00', 1))

    def test_delete_code(self):
        self.db.saveCode('positive', '#00FF00', 1)
        self.db.deleteCode(codeId=1)
        self.assertEqual(0, self.getNumRows('code'))

    def test_update_code_name(self):
        oldName = 'oldName'
        newName = 'newName'
        color = '#00FF00'
        projectId = 1
        self.db.saveCode(oldName, color, projectId)
        self.db.updateCode(1, newName, color)
        self.assertTrue(self.codeExists(1, newName, color, projectId))

    def test_getProjectCodes_None_Exist(self):
        codes = self.db.getProjectCodes(1)
        self.assertEqual(len(codes), 0)

    def test_getProjectCodes_Two_Exist(self):
        self.db.saveCode('code1', '#FFFFFF', 1)
        self.db.saveCode('code2', '#FFFFFF', 1)
        codes = self.db.getProjectCodes(1)
        self.assertEqual(len(codes), 2)
        self.assertEqual(codes[0].name, 'code1')
        self.assertEqual(codes[1].name, 'code2')


if __name__ == '__main__':
    unittest.main()

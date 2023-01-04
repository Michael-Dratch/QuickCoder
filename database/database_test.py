import sqlite3
import unittest
from database import Database
import os


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.db = Database()
        self.db.setConnection(self.conn)

    def assertTableExists(self, name):
        listOfTables = self.cursor.execute(
            """SELECT name FROM sqlite_master WHERE type='table'
            AND name=?; """, (name,)).fetchall()
        self.assertEqual(len(listOfTables), 1)

    def assertFieldExists(self, tableName, fieldName):
        sql_table_description = self.cursor.execute('''SELECT sql FROM sqlite_schema Where name=?''',
                                                    (tableName,)).fetchone()
        self.assertTrue(str(sql_table_description).__contains__(fieldName))


    def tearDown(self):
        self.db.closeConnection()

    def test_createTable(self):
        tableName = 'testTable'
        fields = '(id integer PRIMARY KEY)'
        fieldName = 'id'
        self.db.createTable(tableName, fields)
        self.assertTableExists(tableName)
        self.assertFieldExists(tableName, fieldName)

    def test_createTableCreatesCorrectColumns(self):
        tableName = 'testTable'
        fields = '(id integer PRIMARY KEY, firstName text, lastName text)'
        self.db.createTable(tableName, fields)
        self.assertFieldExists(tableName, 'id')
        self.assertFieldExists(tableName, 'firstName')
        self.assertFieldExists(tableName, 'lastName')

    def test_createCodeTable(self):
        self.db.initializeTables()
        self.assertTableExists("code")
        self.assertTableExists("document")
        self.assertTableExists("project")
        self.assertTableExists("codeinstance")

    def test_save_code(self):
        self.db.saveCode()

if __name__ == '__main__':
    unittest.main()

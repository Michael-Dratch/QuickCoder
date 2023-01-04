import sqlite3
import os


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def createConnection(self, name):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

    def setConnection(self, connection):
        self.conn = connection
        self.cursor = connection.cursor()

    def closeConnection(self):
        self.conn.close()

    def createTable(self, name, fields):
        self.cursor.execute("""CREATE TABLE {} {}""".format(name, fields))

    def initializeTables(self):
        self.createTable('code', '(id integer PRIMARY KEY, name text, color text)')
        self.createTable('document', '(id integer PRIMARY KEY, name text, html text)')
        self.createTable('project', '(id integer PRIMARY KEY, name text)')
        self.createTable('codeinstance', '(id integer PRIMARY KEY, '
                                          'document integer, '
                                          'text text, '
                                          'start integer,'
                                          'end integer)')


    def saveCode(self, Code):
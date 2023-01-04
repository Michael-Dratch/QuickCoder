import sqlite3
from datastructures.code import Code
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
        self.conn.commit()

    def initializeTables(self):
        self.createTable('code', '(id integer PRIMARY KEY, name text, color text, project integer)')
        self.createTable('document', '(id integer PRIMARY KEY, name text, html text)')
        self.createTable('project', '(id integer PRIMARY KEY, name text)')
        self.createTable('codeinstance', '(id integer PRIMARY KEY, '
                                         'document integer, '
                                         'text text, '
                                         'start integer,'
                                         'end integer)')

    def saveCode(self, name, color, projectId):
        sql = """INSERT INTO code (id, name, color, project) VALUES (NULL, :name, :color, :project)"""
        self.cursor.execute(sql, {'project': projectId, 'name': name, 'color': color})
        self.conn.commit()

    def deleteCode(self, codeId):
        sql = """DELETE FROM code WHERE id=:codeId"""
        self.cursor.execute(sql, {'codeId': codeId})
        self.conn.commit()

    def updateCode(self, codeId, name, color):
        sql = """UPDATE code
                    SET name = :name,
                        color = :color
                    WHERE id = :codeId"""
        self.cursor.execute(sql, {'name': name,
                                  'color': color,
                                  'codeId': codeId})
        self.conn.commit()

    def getProjectCodes(self, projectID):
        sql = """SELECT * FROM code WHERE project=:projectID"""
        self.cursor.execute(sql, {'projectID': projectID})
        data = self.cursor.fetchall()
        codes = []
        for row in data:
            code = Code(row[0], row[1], row[2], row[3])
            codes.append(code)
        return codes

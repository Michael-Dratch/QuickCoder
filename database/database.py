import sqlite3
from datastructures.code import Code
import os


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def initializeDatabase(self):
        self.createConnection()
        self.cursor.execute("""PRAGMA foreign_keys = ON""")
        self.conn.commit()

    def createConnection(self, name):
        self.conn = sqlite3.connect(name)
        self.cursor = self.conn.cursor()

    # Used for testing
    def setConnection(self, connection):
        self.conn = connection
        self.cursor = connection.cursor()
        self.cursor.execute("""PRAGMA foreign_keys = ON""")
        self.conn.commit()

    def closeConnection(self):
        self.conn.close()

    def initializeTables(self):
        self.createProjectTable()
        self.createDocumentTable()
        self.createCodeTable()
        self.createCodeInstanceTable()

    def createProjectTable(self):
        self.createTable('project', '(id integer PRIMARY KEY, name text)')

    def createDocumentTable(self):
        self.createTable('document', '(id integer PRIMARY KEY, '
                                     'name text, '
                                     'html text, '
                                     'project_id integer, '
                                     'FOREIGN KEY (project_id) REFERENCES project (id))')

    def createCodeTable(self):
        self.createTable('code', '(id integer PRIMARY KEY, '
                                 'name text, color text, '
                                 'project integer,'
                                 'FOREIGN KEY (project) REFERENCES project (id)) ')

    def createCodeInstanceTable(self):
        self.createTable('codeinstance', '(id integer PRIMARY KEY, '
                                         'document integer, '
                                         'text text, '
                                         'start integer,'
                                         'end integer)')

    def createTable(self, name, fields):
        sql = """CREATE TABLE {} {}""".format(name, fields)
        self.cursor.execute(sql)
        self.conn.commit()

    def createCode(self, name, color, projectId):
        if self.codeExists(name):
            raise Exception('Code name already exists')
        sql = """INSERT INTO code (id, name, color, project) VALUES (NULL, :name, :color, :project)"""
        self.cursor.execute(sql, {'project': projectId, 'name': name, 'color': color})
        self.conn.commit()

    def codeExists(self, name):
        self.cursor.execute("""SELECT * FROM code WHERE name=:name""", {'name': name})
        codes = self.cursor.fetchall()
        return len(codes) > 0

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

    def createProject(self, name):
        if self.project_exists(name):
            raise Exception('Project name already exists')
        sql = """INSERT INTO project (id, name) VALUES (NULL, :name)"""
        self.cursor.execute(sql, {'name': name})
        self.conn.commit()

    def project_exists(self, name):
        self.cursor.execute("""SELECT * FROM project WHERE name=:name""", {'name': name})
        projects = self.cursor.fetchall()
        return len(projects) > 0

    def deleteProject(self, name):
        if not self.project_exists(name):
            return
        sql = """DELETE FROM project WHERE name=:name"""
        self.cursor.execute(sql, {'name': name})
        self.conn.commit()

    def updateProject(self, oldName, newName):
        if not self.project_exists(oldName):
            return
        sql = """UPDATE project
                    SET name = :newName
                    WHERE name = :oldName"""
        self.cursor.execute(sql, {'newName': newName,
                                  'oldName': oldName})
        self.conn.commit()


import sqlite3
from src.datastructures import Code, Project, Document, CodeInstance, Category


class Database:

    def __init__(self):
        self.conn = None
        self.cursor = None

    def initializeDatabase(self, filename):
        self.createConnection(filename)
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
        self.createCategoryTable()
        self.createDocCategoryTable()
        self.createCodeTable()
        self.createCodeInstanceTable()

    def createProjectTable(self):
        self.createTable('project', '(id integer PRIMARY KEY, name text)')

    def createDocumentTable(self):
        self.createTable('document', '(id integer PRIMARY KEY, '
                                     'name text, '
                                     'text text, '
                                     'project integer, '
                                     'FOREIGN KEY (project) REFERENCES project (id) ON DELETE CASCADE)')

    def createCategoryTable(self):
        self.createTable('category', '(id integer PRIMARY KEY,'
                                     'name text)')

    def createDocCategoryTable(self):
        self.createTable('doc_category', '(docID int,'
                                         'categoryID int,'
                                         'PRIMARY KEY (docID, categoryID),'
                                         'FOREIGN KEY (docID) REFERENCES document (id) ON DELETE CASCADE,'
                                         'FOREIGN KEY (categoryID) REFERENCES category (id) ON DELETE CASCADE)')

    def createCodeTable(self):
        self.createTable('code', '(id integer PRIMARY KEY, '
                                 'name text, '
                                 'color text, '
                                 'project integer,'
                                 'FOREIGN KEY (project) REFERENCES project (id) ON DELETE CASCADE) ')

    def createCodeInstanceTable(self):
        self.createTable('codeinstance', '(id integer PRIMARY KEY, '
                                         'document integer, '
                                         'code integer,'
                                         'text text, '
                                         'start integer,'
                                         'end integer,'
                                         'sentiment text,'
                                         'FOREIGN KEY (document) REFERENCES document (id) ON DELETE CASCADE, '
                                         'FOREIGN KEY (code) REFERENCES code (id) ON DELETE CASCADE) ')

    def createTable(self, name, fields):
        sql = """CREATE TABLE {} {}""".format(name, fields)
        self.cursor.execute(sql)
        self.conn.commit()

    def createCode(self, name, color, projectID):
        if self.codeExistsByName(name, projectID):
            raise Exception('Code name already exists')
        sql = """INSERT INTO code (id, name, color, project) VALUES (NULL, :name, :color, :project)"""
        self.cursor.execute(sql, {'project': projectID, 'name': name, 'color': color})
        self.conn.commit()
        codeID = self.cursor.lastrowid
        code = Code(codeID, name, color)
        return code

    def getProjectIDFromName(self, projectName):
        self.cursor.execute("""SELECT * FROM project WHERE name=:projectName""", {'projectName': projectName})
        projectID = self.cursor.fetchone()
        return projectID

    def getCode(self, codeID):
        self.cursor.execute("""SELECT * FROM code WHERE id=:codeID""",
                            {'codeID': codeID})
        codeData = self.cursor.fetchone()
        code = Code(codeData[0], codeData[1], codeData[2])
        return code

    def codeExistsByID(self, codeID):
        self.cursor.execute("""SELECT * FROM code WHERE id=:codeID""",
                            {'codeID': codeID})
        codes = self.cursor.fetchall()
        return len(codes) > 0

    def codeExistsByName(self, name, projectID):
        self.cursor.execute("""SELECT * FROM code 
                                WHERE name=:name AND project=:projectID""",
                            {'name': name, 'projectID': projectID})
        codes = self.cursor.fetchall()
        return len(codes) > 0

    def deleteCode(self, codeID):
        sql = """DELETE FROM code 
                    WHERE id = :codeID"""
        self.cursor.execute(sql, {'codeID': codeID})
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
            code = Code(row[0], row[1], row[2])
            codes.append(code)
        return codes

    def createProject(self, name):
        if self.projectExistsByName(name):
            raise Exception('Project name already exists')
        sql = """INSERT INTO project (id, name) VALUES (NULL, :name)"""
        self.cursor.execute(sql, {'name': name})
        self.conn.commit()
        projectID = self.cursor.lastrowid
        return Project(projectID, name)

    def projectExists(self, projectID):
        self.cursor.execute("""SELECT * FROM project WHERE id=:projectID""", {'projectID': projectID})
        projects = self.cursor.fetchall()
        return len(projects) > 0

    def projectExistsByName(self, name):
        self.cursor.execute("""SELECT * FROM project WHERE name=:name""", {'name': name})
        projects = self.cursor.fetchall()
        return len(projects) > 0

    def deleteProject(self, projectID):
        sql = """DELETE FROM project WHERE id=:projectID"""
        self.cursor.execute(sql, {'projectID': projectID})
        self.conn.commit()

    def updateProject(self, projectID, newName):
        if not self.projectExists(projectID):
            return
        sql = """UPDATE project
                    SET name = :newName
                    WHERE id = :projectID"""
        self.cursor.execute(sql, {'newName': newName,
                                  'projectID': projectID})
        self.conn.commit()

    def getProjects(self):
        sql = """SELECT * FROM project"""
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        projects = []
        for object in data:
            project = Project(object[0], object[1])
            projects.append(project)
        return projects

    def createDocument(self, name, projectID):
        if self.documentExistsByName(name, projectID):
            raise Exception('Document name already exists')
        sql = """INSERT INTO document (id, name, text, project) VALUES (NULL, :name, :text, :project)"""
        self.cursor.execute(sql, {'name': name, 'text': '', 'project': projectID})
        self.conn.commit()
        docID = self.cursor.lastrowid
        return Document(docID, name, '')

    def documentExistsByID(self, documentID):
        self.cursor.execute("""SELECT * FROM document WHERE id=:documentID""",
                            {'documentID': documentID})
        documents = self.cursor.fetchall()
        return len(documents) > 0

    def getDocumentByID(self, documentID):
        self.cursor.execute("""SELECT * FROM document WHERE id=:documentID""",
                            {'documentID': documentID})
        documentData = self.cursor.fetchone()
        document = Document(documentData[0], documentData[1], documentData[2])
        return document

    def documentExistsByName(self, name, projectID):
        self.cursor.execute("""SELECT * FROM document WHERE name=:name AND project=:projectID""",
                            {'name': name, 'projectID': projectID})
        documents = self.cursor.fetchall()
        return len(documents) > 0

    def updateDocumentName(self, documentID, newName, projectID):
        if self.documentExistsByName(newName, projectID):
            raise DuplicateNameError()
        sql = """UPDATE document
                           SET name = :newName
                           WHERE id = :id"""
        self.cursor.execute(sql, {'newName': newName, 'id': documentID})
        self.conn.commit()

    def updateDocumentText(self, documentID, text):
        sql = """UPDATE document 
                    SET text = :text
                    WHERE id = :id"""
        self.cursor.execute(sql, {'text': text, 'id': documentID})
        self.conn.commit()

    def deleteDocument(self, documentID):
        sql = """DELETE FROM document WHERE id=:documentID"""
        self.cursor.execute(sql, {'documentID': documentID})
        self.conn.commit()

    def getProjectDocuments(self, projectID):
        sql = """SELECT * FROM document WHERE project=:projectID"""
        self.cursor.execute(sql, {'projectID': projectID})
        data = self.cursor.fetchall()
        docs = []
        for docObject in data:
            document = Document(docObject[0], docObject[1], docObject[2])
            docs.append(document)
        return docs

    def createCategory(self, name):
        sql = """INSERT INTO category (id, name)
                    VALUES(NULL, :name)"""
        self.cursor.execute(sql, {'name': name})
        self.conn.commit()
        category = Category(self.cursor.lastrowid, name)
        return category

    def deleteCategory(self, categoryID):
        sql = """DELETE FROM category WHERE id=:categoryID"""
        self.cursor.execute(sql, {'categoryID': categoryID})
        self.conn.commit()

    def updateCategoryName(self, categoryID, newName):
        sql = """UPDATE category
                    SET name = :newName
                    WHERE id = :categoryID"""
        self.cursor.execute(sql, {'newName': newName, 'categoryID': categoryID})

    def createDocCategory(self, docID, categoryID):
        sql = """INSERT INTO doc_category(docID, categoryID)
                    VALUES (:docID, :categoryID)"""
        self.cursor.execute(sql, {'docID': docID, 'categoryID': categoryID})
        self.conn.commit()

    def deleteDocCategory(self, docID, categoryID):
        sql = """DELETE FROM doc_category
                    WHERE docID = :docID
                    AND categoryID = :categoryID"""
        self.cursor.execute(sql, {'docID': docID, 'categoryID': categoryID})
        self.conn.commit()

    def getDocumentCategories(self, docID):
        sql = """SELECT c.id, c.name 
                FROM doc_category d JOIN category c ON d.categoryID = c.id
                WHERE docID = :docID"""
        self.cursor.execute(sql, {'docID': docID})
        data = self.cursor.fetchall()
        categories = []
        for item in data:
            category = Category(item[0], item[1])
            categories.append(category)
        return categories


    def createCodeInstance(self, document, code, text, start, end, sentiment):
        sql = """INSERT INTO codeinstance (id, document, code, text, start, end, sentiment) 
                    VALUES (NULL, :documentID, :codeID, :text, :start, :end, :sentiment)"""
        self.cursor.execute(sql, {'documentID': document.id,
                                  'codeID': code.id,
                                  'text': text,
                                  'start': start,
                                  'end': end,
                                  'sentiment': sentiment})
        self.conn.commit()
        codeInstance = CodeInstance(self.cursor.lastrowid, text, start, end, None, code)
        return codeInstance

    def getDocumentCodeInstances(self, documentID):
        sql = """SELECT code.id, 
                        code.name, 
                        code.color,
                        codeinstance.id,
                        codeinstance.text,
                        codeinstance.start,
                        codeinstance.end,
                        codeinstance.sentiment
                FROM codeinstance 
                INNER JOIN code ON codeinstance.code = code.id 
                WHERE document=:documentID"""
        self.cursor.execute(sql, {'documentID': documentID})
        data = self.cursor.fetchall()
        return self.buildCodeInstanceObjects(data)

    def getDocumentCodeInstancesByCode(self, documentID, codeID):
        sql = """SELECT code.id, 
                         code.name, 
                         code.color,
                         codeinstance.id,
                         codeinstance.text,
                         codeinstance.start,
                         codeinstance.end,
                         codeinstance.sentiment
                 FROM codeinstance 
                 INNER JOIN code ON codeinstance.code = code.id 
                 WHERE document=:documentID
                 AND code=:codeID"""
        self.cursor.execute(sql, {'documentID': documentID, 'codeID': codeID})
        data = self.cursor.fetchall()
        return self.buildCodeInstanceObjects(data)

    def buildCodeInstanceObjects(self, data):
        codeInstances = []
        for row in data:
            code = Code(row[0], row[1], row[2])
            codeInstance = CodeInstance(row[3], row[4], row[5], row[6], row[7], code)
            codeInstances.append(codeInstance)
        return codeInstances

    def deleteCodeInstance(self, instanceId):
        sql = """DELETE FROM codeinstance WHERE id=:id"""
        self.cursor.execute(sql, {'id': instanceId})
        self.conn.commit()

    def deleteAllInstancesOfCode(self, codeID):
        sql = """DELETE FROM codeinstance WHERE code=:codeID"""
        self.cursor.execute(sql, {'codeID': codeID})
        self.conn.commit()

    def getProjectCodeInstances(self, projectID):
        sql = """SELECT code.id, 
                        code.name, 
                        code.color,
                        codeinstance.id,
                        codeinstance.text,
                        codeinstance.start,
                        codeinstance.end,
                        codeinstance.sentiment
                FROM codeinstance 
                INNER JOIN document ON codeinstance.document = document.id
                INNER JOIN code ON codeinstance.code = code.id 
                WHERE document.project=:projectID"""
        self.cursor.execute(sql, {'projectID': projectID})
        data = self.cursor.fetchall()
        return self.buildCodeInstanceObjects(data)


class DuplicateNameError(Exception):
    def __init__(self):
        super().__init__()

import sqlite3
import unittest
from src.datastructures import *
from src.database.database import Database


class TestBase(unittest.TestCase):

    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.db = Database()
        self.db.setConnection(self.conn)
        self.db.initializeTables()

    def tearDown(self):
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

    def codeExistsByID(self, codeID):
        self.cursor.execute("""SELECT * FROM code WHERE id=:codeID""",
                            {'codeID': codeID})
        data = self.cursor.fetchall()
        return len(data) == 1

    def codeExistsByName(self, name):
        self.cursor.execute("""SELECT * FROM code WHERE name=:name""",
                            {'name': name})
        data = self.cursor.fetchall()
        return len(data) == 1

    def projectExists(self, name):
        self.cursor.execute("""SELECT * FROM project WHERE name=:name""", {'name': name})
        data = self.cursor.fetchall()
        return len(data) == 1

    def documentExistsByID(self, documentID):
        self.cursor.execute("""SELECT * FROM document WHERE id=:documentID""",
                            {'documentID': documentID})
        data = self.cursor.fetchall()
        return len(data) == 1

    def documentExistsByName(self, name):
        self.cursor.execute("""SELECT * FROM document WHERE name=:name""",
                            {'name': name})
        data = self.cursor.fetchall()
        return len(data) == 1

    def getNumRows(self, tableName):
        self.cursor.execute("""SELECT * FROM {}""".format(tableName))
        data = self.cursor.fetchall()
        return len(data)


class DatabaseTest(TestBase):

    def test_Tables_created(self):
        self.assertTableExists("code")
        self.assertTableExists("document")
        self.assertTableExists("project")
        self.assertTableExists("codeinstance")


class ProjectTableTest(TestBase):

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

    def test_foreign_key_constraint_on_code(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.createCode('name', 'blue', 2)

    def test_create_project(self):
        self.db.createProject('test_project')
        projects = self.db.getProjects()
        self.assertTrue(self.projectExists('test_project'))

    def test_creating_duplicate_project_fails(self):
        self.db.createProject('project')
        with self.assertRaises(Exception):
            self.db.createProject('project')

    def test_delete_non_existent_project_does_nothing(self):
        self.db.deleteProject('project')

    def test_delete_project(self):
        self.db.createProject('project')
        self.db.deleteProject(1)
        projects = self.db.getProjects()
        self.assertEqual(len(projects), 0)

    def test_update_non_existent_project_does_nothing(self):
        self.db.updateProject(1, 'newName')

    def test_update_project_name(self):
        self.db.createProject('oldName')
        self.db.updateProject(1, 'newName')
        projects = self.db.getProjects()
        self.assertEqual(projects[0].name, 'newName')


#
class DocumentTableTest(TestBase):

    def setUp(self):
        super().setUp()
        self.db.createProject('project')

    def test_create_document(self):
        self.db.createDocument('doc', 1)
        self.assertTrue(self.documentExistsByName('doc'))

    def test_create_duplicate_document_fails(self):
        self.db.createCode('code', 'blue', 1)
        with self.assertRaises(Exception):
            self.db.createCode('code', 'green', 1)

    def test_foreign_key_constraint_on_document(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.createDocument('name', 2)

    def test_update_Document_Name(self):
        oldName = 'oldName'
        newName = 'newName'
        self.db.createDocument(oldName, 1)
        self.db.updateDocumentName(1, newName, 1)
        self.assertFalse(self.documentExistsByName(oldName))
        self.assertTrue(self.documentExistsByName(newName))

    def test_update_Document_duplicate_name_denied(self):
        oldName = 'oldName'
        newName = 'newName'
        self.db.createDocument(oldName, 1)
        self.db.createDocument(newName, 1)
        with self.assertRaises(Exception):
            self.db.updateDocumentName(1, newName, 1)

    def test_update_document_duplicate_name_different_project_allowed(self):
        self.db.createProject('project2')
        oldName = 'oldName'
        newName = 'newName'
        self.db.createDocument(oldName, 1)
        self.db.createDocument(newName, 2)
        self.db.updateDocumentName(1, newName, 1)

    def test_delete_document(self):
        self.db.createDocument('doc', 1)
        self.db.deleteDocument(1)
        self.assertFalse(self.documentExistsByID(1))

    def test_get_documents_no_docs(self):
        documents = self.db.getProjectDocuments(1)
        self.assertEqual(len(documents), 0)

    def test_get_documents(self):
        self.db.createDocument('doc1', 1)
        self.db.createDocument('doc2', 1)
        docs = self.db.getProjectDocuments(1)
        self.assertEqual(len(docs), 2)


class CodeTableTest(TestBase):

    def setUp(self):
        super().setUp()
        self.db.createProject('test_project')

    def test_create_code(self):
        self.db.createCode('positive', '#00FF00', 1)
        self.assertTrue(self.codeExistsByName('positive'))

    def test_create_duplicate_code_fails(self):
        self.db.createCode('code', 'blue', 1)
        with self.assertRaises(Exception):
            self.db.createCode('code', 'green', 1)

    def test_delete_code(self):
        self.db.createCode('positive', '#00FF00', 1)
        self.db.deleteCode(codeID=1)
        self.assertEqual(0, self.getNumRows('code'))

    def test_update_code_name(self):
        oldName = 'oldName'
        newName = 'newName'
        color = '#00FF00'
        projectId = 1
        self.db.createCode(oldName, color, projectId)
        self.db.updateCode(1, newName, color)
        self.assertTrue(self.codeExistsByName(newName))


class CodeInstanceTableTest(TestBase):

    def setUp(self):
        super().setUp()
        self.db.createProject('test_project')
        self.currentCode = self.db.createCode('code', '#FF00FF', 1)
        self.currentDoc = self.db.createDocument('doc', 1)

    def test_create_code_instance(self):
        self.db.createCodeInstance(self.currentDoc, self.currentCode, "test_text", 5, 20, None)
        self.cursor.execute("""SELECT * FROM codeinstance""")
        codeInstances = self.cursor.fetchall()
        self.assertEqual(len(codeInstances), 1)

    def test_get_code_document_instances(self):
        self.db.createCodeInstance(self.currentDoc, self.currentCode, "test_text", 5, 20, None)
        codeInstance = self.db.getDocumentCodeInstances(1)[0]
        self.assertEqual(codeInstance.text, 'test_text')
        self.assertEqual(codeInstance.start, 5)
        self.assertEqual(codeInstance.end, 20)
        self.assertEqual(codeInstance.code.name, 'code')

    def test_delete_codeInstance(self):
        self.db.createCodeInstance(self.currentDoc, self.currentCode, "test_text", 5, 20, None)
        self.db.deleteCodeInstance(1)
        self.cursor.execute("""SELECT * FROM codeinstance""")
        instances = self.cursor.fetchall()
        self.assertEqual(len(instances), 0)

    def test_deleting_non_existent_codeInstance_doesnt_break(self):
        self.db.deleteCodeInstance(1)
        self.cursor.execute("""SELECT * FROM codeinstance""")
        instances = self.cursor.fetchall()
        self.assertEqual(len(instances), 0)

    def test_get_Project_code_instance(self):
        doc2 = self.db.createDocument('doc2', 1)
        self.db.createCodeInstance(self.currentDoc, self.currentCode, 'text', 5, 20, None)
        self.db.createCodeInstance(doc2, self.currentCode, 'text2', 5, 20, None)
        self.db.createProject('project2')
        doc3 = self.db.createDocument('doc3', 2)
        code3 = self.db.createCode('code3', 'color', 2)
        self.db.createCodeInstance(doc3, code3, 'project2Instance', 5, 10, None)
        codeInstances = self.db.getProjectCodeInstances(1)
        self.assertEqual(len(codeInstances), 2)


class CategoriesTest(TestBase):
    def createInitialDataForDocCategories(self):
        self.db.createProject('project1')
        self.db.createDocument('doc1', 1)
        self.db.createCategory('category1')

    def assertDocCategoryCorrect(self, data, docID, catID):
        self.assertEqual(docID, data[0])
        self.assertEqual(catID, data[1])

    def setUp(self):
        super().setUp()

    def test_create_category(self):
        self.db.createCategory('category1')
        self.cursor.execute("""SELECT * FROM category""")
        data = self.cursor.fetchall()
        categoryData = data[0]
        self.assertEqual(categoryData[0], 1)
        self.assertEqual(categoryData[1], 'category1')

    def test_delete_category(self):
        self.db.createCategory('category1')
        self.db.deleteCategory(1)
        self.cursor.execute("""SELECT * FROM category""")
        data = self.cursor.fetchall()
        self.assertEqual(0, len(data))

    def test_update_category_name(self):
        self.db.createCategory('old_name')
        self.db.updateCategoryName(1, 'new_name')
        self.cursor.execute("""Select * FROM category""")
        data = self.cursor.fetchone()
        self.assertEqual('new_name', data[1])

    def test_create_docCategory(self):
        self.createInitialDataForDocCategories()
        self.db.createDocCategory(1, 1)
        self.cursor.execute("""SELECT * FROM doc_category""")
        data = self.cursor.fetchone()
        self.assertDocCategoryCorrect(data, 1, 1)

    def test_delete_docCategory(self):
        self.createInitialDataForDocCategories()
        self.db.createDocCategory(1, 1)
        self.db.deleteDocCategory(1, 1)
        self.cursor.execute("""SELECT * FROM doc_category""")
        data = self.cursor.fetchall()
        self.assertEqual(0, len(data))

    def test_get_all_doc_categories(self):
        self.createInitialDataForDocCategories()
        self.db.createCategory('category2')
        self.db.createDocCategory(1, 1)
        self.db.createDocCategory(1, 2)
        categories = self.db.getDocumentCategories(1)
        self.assertEqual(2, len(categories))
        self.assertEqual(categories[0].name, 'category1')
        self.assertEqual(categories[1].name, 'category2')

class DocTreeTest(TestBase):
    def setUp(self):
        super().setUp()
        self.db.createProject('project')
        self.data = {
            'folder1': {},
            'folder2': {'doc1': 1},
            'folder3': {'folder4': {}},
            'folder5': {'folder6': {'doc2': 2}},
            'doc3': 3
        }
    def test_create_doc_table(self):
        self.db.createNew()

if __name__ == '__main__':
    unittest.main()

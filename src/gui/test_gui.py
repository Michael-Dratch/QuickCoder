import sys
import unittest

from PyQt6.QtGui import QTextCursor
from PyQt6.QtWidgets import QWidget, QApplication

from src.datastructures import CodeInstance, Code, Document
from src.gui.editor import Editor


class TestGUI(unittest.TestCase):

    def createCodeInstanceHandler(self, start, end, text):
        self.instanceStart = start
        self.instanceEnd = end
        self.instanceText = text

    def saveCodeInstancesHandler(self, codeInstances):
        print('saving code instances')

    def createCodeInstances(self):
        instance1 = CodeInstance(1,
                                 'd be form’d, till the ductile anchor hold, Till the gossamer thread you fling catch somewhere, O',
                                 447, 543, Code(1, 'code1', '#FFAAAA'))
        instance2 = CodeInstance(2,
                                 'sdlfisdj',
                                 5, 10, Code(2, 'code2', "#AAAAEE"))
        return [instance1, instance2]

    def createDocument(self):
        doc = Document(1, 'doc1', """A noiseless patient spider,
        I mark’d where on a little promontory it stood isolated,
        Mark’d how to explore the vacant vast surrounding,
        It launch’d forth filament, filament, filament, out of itself,
        Ever unreeling them, ever tirelessly speeding them.

        And you O my soul where you stand,
        Surrounded, detached, in measureless oceans of space,
        Ceaselessly musing, venturing, throwing, seeking the spheres to connect them,
        Till the bridge you will need be form’d, till the ductile anchor hold,
        Till the gossamer thread you fling catch somewhere, O my soul.
        """)
        return doc

    def selectTextRange(self, end, start):
        cursor = self.editor.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        self.editor.setTextCursor(cursor)


    def assertCreateCodeHandlerCalledCorrectly(self, doc, end, start):
        self.assertTrue(self.instanceStart, start)
        self.assertTrue(self.instanceEnd, end)
        self.assertTrue(self.instanceText, doc.html[start:end])

    def assertEqualRange(self, instanceAfter, instanceBefore):
        self.assertEqual(instanceAfter.start, instanceBefore.start)
        self.assertEqual(instanceAfter.end, instanceBefore.end)

    def setUp(self):
        self.app = QApplication(sys.argv)
        self.window = QWidget()
        self.editor = Editor(self.window, self.createCodeInstanceHandler, self.saveCodeInstancesHandler)
        self.code1 = Code(1, 'code1', '#00FF00')
        self.doc = self.createDocument()
        self.editor.setDocument(self.doc)

    def test_setInstances(self):
        instances = self.createCodeInstances()
        self.editor.setCodeInstances(instances)
        self.assertEqual(instances, self.editor.codeInstances)

    def test_code_text(self):
        start = 2
        end = 5
        self.selectTextRange(end, start)
        self.editor.codeSelectedText()
        self.assertCreateCodeHandlerCalledCorrectly(self.doc, end, start)

    def test_no_instance_changed_after_deletion_after_instance(self):
        instanceBefore = CodeInstance(1, 'noi', 2, 5, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(10, 15)
        self.editor.cut()
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqualRange(instanceAfter, instanceBefore)

    def test_no_instance_changed_after_insertion_after_instance(self):
        instanceBefore = CodeInstance(1, 'noi', 2, 5, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(10, 10)
        self.editor.insertHtml('insertion_text')
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqualRange(instanceAfter, instanceBefore)

    def test_insertion_before_instance_editor_correctly_updates_instance(self):
        insertionText = 'insertion_text'
        startBeforeChange = 2
        endBeforeChange = 5
        instanceBefore = CodeInstance(1, 'noi', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(0,0)
        self.editor.insertHtml(insertionText)
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, startBeforeChange + len(insertionText))
        self.assertEqual(instanceAfter.end, endBeforeChange + len(insertionText))

    def test_deletion_before_instance_editor_correctly_updates_instance(self):
        startBeforeChange = 3
        endBeforeChange = 6
        charsDeleted = 2
        instanceBefore = CodeInstance(1, 'ois', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(0, charsDeleted)
        self.editor.cut()
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, startBeforeChange - charsDeleted)
        self.assertEqual(instanceAfter.end, endBeforeChange - charsDeleted)

    def test_insertion_inside_instance_range_correctly_updates_range(self):
        insertionText = 'insertion_text'
        startBeforeChange = 2
        endBeforeChange = 6
        instanceBefore = CodeInstance(1, 'nois', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(3, 3)
        self.editor.insertHtml(insertionText)
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, startBeforeChange)
        self.assertEqual(instanceAfter.end, endBeforeChange + len(insertionText))
        self.assertEqual(instanceAfter.text, 'ninsertion_textois')

    def test_delete_inside_instance_correctly_updates_range(self):
        startBeforeChange = 2
        endBeforeChange = 6
        charsDeleted = 2
        instanceBefore = CodeInstance(1, 'nois', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(3, 3 + charsDeleted)
        self.editor.cut()
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, startBeforeChange)
        self.assertEqual(instanceAfter.end, endBeforeChange - charsDeleted)
        self.assertEqual(instanceAfter.text, 'ns')

    def test_delete_beginning_portion_of_text_correctly_updates(self):
        startBeforeChange = 2
        endBeforeChange = 6
        charsDeleted = 4
        deletionPosition = 0
        instanceBefore = CodeInstance(1, 'nois', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(deletionPosition, deletionPosition + charsDeleted)
        self.editor.cut()
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, deletionPosition)
        self.assertEqual(instanceAfter.end, endBeforeChange - charsDeleted)
        self.assertEqual(instanceAfter.text, 'is')

    def test_delete_end_portion_of_text_correctly_updates_range(self):
        startBeforeChange = 2
        endBeforeChange = 6
        charsDeleted = 10
        deletionPosition = 3
        instanceBefore = CodeInstance(1, 'nois', startBeforeChange, endBeforeChange, self.code1)
        self.editor.setCodeInstances([instanceBefore])
        self.selectTextRange(deletionPosition, deletionPosition + charsDeleted)
        self.editor.cut()
        instanceAfter = self.editor.codeInstances[0]
        self.assertEqual(instanceAfter.start, startBeforeChange)
        self.assertEqual(instanceAfter.end, deletionPosition)
        self.assertEqual(instanceAfter.text, 'n')



if __name__ == "__main__":
    unittest.main()

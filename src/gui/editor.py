from functools import partial

from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextCharFormat, QTextFormat, QColor, QTextCursor, QShortcut, QKeySequence


class Editor(QTextEdit):
    def __init__(self, parent, createCodeInstanceHandler):
        super(Editor, self).__init__(parent)
        self.createCodeInstanceHandler = createCodeInstanceHandler
        self.codeInstances = []
        self.currentCode = None
        self.setStyleSheet("padding: 20px;"
                           "background-color: white;")

        self.codeShortcut = QShortcut(QKeySequence('Ctrl+H'), self)
        self.codeShortcut.activated.connect(self.codeSelectedText)
        self.document = self.document()
        self.document.contentsChange.connect(self.contentsChangedHandler)
        self.documentSet = False


    def setDocument(self, doc):
        self.documentSet = False
        self.setText(doc.text)
        self.documentSet = True

    def setCurrentCode(self, code):
        self.currentCode = code
    def setCodeInstances(self, codeInstances):
        self.codeInstances = codeInstances

    def highlightAllCodeInstances(self):
        self.removeAllHighlights()
        for instance in self.codeInstances:
            self.highlightRange(instance.start, instance.end, instance.code.color)
        self.setSelection(0, 0)

    def highlightCodeInstances(self, code):
        for instance in self.codeInstances:
            if instance.code.id == code.id:
                self.highlightRange(instance.start, instance.end, instance.code.color)
        self.setSelection(0, 0)

    def highlightRange(self, start, end, color):
        self.setSelection(start, end)
        self.highlightSelection(color)

    def setSelection(self, start, end):
        cursor = self.textCursor()
        cursor.setPosition(start)
        cursor.setPosition(end, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def highlightSelection(self, color):
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QColor(color))
        cursor.setCharFormat(fmt)
        self.setFocus()

    def codeSelectedText(self):
        if self.currentCode is None:
            return
        range = self.getSelectedRange()
        if range.start == range.end:
            return
        text = self.getSelectedText()
        self.highlightSelection(self.currentCode.color)
        self.createCodeInstanceHandler(range.start, range.end, text)

    def getSelectedRange(self):
        cursor = self.textCursor()
        return Range(cursor.selectionStart(), cursor.selectionEnd())

    def getSelectedText(self):
        cursor = self.textCursor()
        return cursor.selectedText()

    def removeAllHighlights(self):
        self.selectAll()
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QColor("white"))
        cursor.setCharFormat(fmt)
        self.setFocus()

    def contentsChangedHandler(self, pos, removed, added):
        if self.documentSet == False:
            return
        for instance in self.codeInstances:
            if instance.end < pos:
                continue
            if added > 0:
                self.processInsertion(added, instance, pos)
            if removed > 0:
                self.processDeletion(instance, pos, removed)

    def processInsertion(self, added, instance, pos):
        if pos < instance.start:  # instance after insertion
            instance.start += added
            instance.end += added
            self.updateCodeInstanceText(instance)
        else:
            instance.end += added  # insertion in the middle of range, add only to range
            self.updateCodeInstanceText(instance)


    def processDeletion(self, instance, pos, removed):
        if pos < instance.start:
            if removed < (instance.start - pos):  # deletion fully before instance range
                instance.start -= removed
                instance.end -= removed
            elif removed < (instance.end - pos):
                instance.start = pos
                instance.end -= removed
                self.updateCodeInstanceText(instance)
            else:
                self.showDeleteDialog(instance)
        else:
            if removed < (instance.end - pos):
                instance.end -= removed
                self.updateCodeInstanceText(instance)
            else:
                instance.end = pos
                self.updateCodeInstanceText(instance)

    def updateCodeInstanceText(self, instance):
        self.setSelection(instance.start, instance.end)
        text = self.getSelectedText()
        instance.text = text
    def showDeleteDialog(self, instance):
        dlg = DeleteCodeInstanceDialog()
        if dlg.exec():
            self.codeInstances.remove(instance)
        else:
            self.undo()

    def updateCodeInstanceColor(self, updatedCode):
        for instance in self.codeInstances:
            if instance.code.id == updatedCode.id:
                instance.code.color = updatedCode.color
        self.highlightAllCodeInstances()

    def removeCodeInstance(self, codeInstance):
        print('removing code instance')
        print('current code instance')
        for i in self.codeInstances:
            print(i.text)
        print('instance to delete:' + codeInstance.text)
        self.codeInstances.remove(codeInstance)
        self.highlightAllCodeInstances()


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end


class DeleteCodeInstanceDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("")
        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.setCenterButtons(True)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        message = QLabel("""This deletion will remove all information about previously coded text within the deleted section. Press ok to perform deletion.""")
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

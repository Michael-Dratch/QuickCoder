from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextCharFormat, QTextFormat, QColor, QTextCursor, QShortcut, QKeySequence


class Editor(QTextEdit):
    def __init__(self, parent, createCodeInstanceHandler):
        super(Editor, self).__init__(parent)
        self.createCodeInstanceHandler = createCodeInstanceHandler
        self.codeInstances = []
        self.setStyleSheet("padding: 20px;"
                           "background-color: white;")

        self.codeShortcut = QShortcut(QKeySequence('Ctrl+H'), self)
        self.codeShortcut.activated.connect(self.codeSelectedText)


    def setCodeInstances(self, codeInstances):
        self.codeInstances = codeInstances



    def highlightCodeInstances(self):
        for instance in self.codeInstances:
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
        range = self.getSelectedRange()
        if range.start == range.end:
            return
        text = self.getSelectedText()
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


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

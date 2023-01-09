from PyQt6.QtWidgets import *
from PyQt6.QtGui import QTextCharFormat, QTextFormat, QColor, QTextCursor


class Editor(QTextEdit):
    def __init__(self, parent):
        super(Editor, self).__init__(parent)
        self.setStyleSheet('QTextEdit{padding: 50px}')
    def printSelection(self):
        cursor = self.textCursor()
        print(cursor.selectedText())

    def highlightSelection(self):
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QColor("yellow"))
        cursor.setCharFormat(fmt)
        self.setFocus()

    def highlightRange(self, range):
        self.setSelection(range)
        self.highlightSelection()

    def removeAllHighlights(self):
        self.selectAll()
        cursor = self.textCursor()
        fmt = cursor.charFormat()
        fmt.setBackground(QColor("white"))
        cursor.setCharFormat(fmt)
        self.setFocus()

    def setSelection(self, range):
        cursor = self.textCursor()
        cursor.setPosition(range.start)
        cursor.setPosition(range.end, QTextCursor.MoveMode.KeepAnchor)
        self.setTextCursor(cursor)

    def getSelectedText(self):
        cursor = self.textCursor()
        return cursor.selectedText()

    def getSelectedRange(self):
        cursor = self.textCursor()
        return Range(cursor.selectionStart(), cursor.selectionEnd())


class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

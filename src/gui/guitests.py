from src.datastructures import Code
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.testwindowbuilder import TestWindowBuilder


def getNewCodeList():
    code1 = Code(1, 'code1', '#FF00FF')
    code2 = Code(2, 'code2', '#FF00FF')
    return [code1, code2]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    builder = TestWindowBuilder()
    GUI = builder.build()

    codes = getNewCodeList()

    codeListView = builder.codeListView
    codeListView.setCodes(codes)
    GUI.show()
    sys.exit(app.exec())



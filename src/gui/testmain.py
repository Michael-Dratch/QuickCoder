import unittest

from src.datastructures import Code, CodeInstance, Document, Sentiment
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.testwindowbuilder import TestWindowBuilder


class Main():

    def run(self):
        app = QApplication(sys.argv)
        builder = TestWindowBuilder()
        GUI = builder.build()
        self.code3 = Code(3, 'code3', '#AAFFAA')
        self.instancesView = builder.instanceView
        self.codeInstances = self.createCodeInstances()
        self.instancesView.setCodeInstances(self.codeInstances)


        GUI.show()

        sys.exit(app.exec())

    def createCodeInstances(self):
        instance1 = CodeInstance(1,
                                 'd be form’d, till the ductile anchor hold, Till the gossame ductileld, Till '
                                 'Till the gossame ductileld, Till the gossame ductile anchor holthe gossame ductile anchor hold, Till  anchor hold, Till the gossamer thread you flier thread you fling catch somewhere, O',
                                 447, 543, Sentiment.POSITIVE, Code(1, 'code1', '#FFAAAA'))
        instance2 = CodeInstance(2,
                                 'sdlfisdj',
                                 5, 10, Sentiment.NEGATIVE, Code(2, 'code2', "#AAAAEE"))
        instance3 = CodeInstance(3,
                                 'sdlfisdj',
                                 20, 30, Sentiment.NEUTRAL, Code(2, 'code2', "#AAAAEE"))
        instance4 = CodeInstance(3,
                                 'sdlfisdj',
                                 35, 40, None, Code(2, 'code2', "#AAAAEE"))
        return [instance1, instance2, instance3, instance4]




if __name__ == "__main__":
    main = Main()
    main.run()

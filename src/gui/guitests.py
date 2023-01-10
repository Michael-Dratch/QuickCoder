from src.datastructures import Code, CodeInstance
import sys
from PyQt6.QtWidgets import QApplication
from src.gui.testwindowbuilder import TestWindowBuilder


class Main:

    def run(self):
        app = QApplication(sys.argv)
        builder = TestWindowBuilder(self.createCodeInstanceHandler)
        GUI = builder.build()

        self.editor = builder.editor
        self.codes = self.createCodeInstances()
        self.editor.setCodeInstances(self.codes)

        self.editor.setText("""A noiseless patient spider,
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

        GUI.show()

        self.editor.highlightCodeInstances()
        sys.exit(app.exec())

    def createCodeInstances(self):
        instance1 = CodeInstance(1,
                                 'd be form’d, till the ductile anchor hold, Till the gossamer thread you fling catch somewhere, O',
                                 447, 543, Code(1, 'code1', '#FFAAAA'))
        instance2 = CodeInstance(2,
                                 'sdlfisdj',
                                 5, 10, Code(2, 'code2', "#AAAAEE"))
        return [instance1, instance2]

    def createCodeInstanceHandler(self, start, end, text):
        instance = CodeInstance(3, text, start, end, Code(3, 'code3', '#AAFFAA'))
        self.codes.append(instance)
        self.editor.setCodeInstances(self.codes)
        self.editor.removeAllHighlights()
        self.editor.highlightCodeInstances()


if __name__ == "__main__":
    main = Main()
    main.run()

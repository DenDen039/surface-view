import package.ui.gui as gui
from PyQt5.QtWidgets import QApplication
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    UIWindow = gui.UI()
    app.exec_()
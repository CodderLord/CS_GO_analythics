from qt.global_window import LinkInputWindow
from PyQt6.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    window = LinkInputWindow()
    APP.exec()

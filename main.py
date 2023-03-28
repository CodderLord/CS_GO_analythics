from qt.global_window import LinkInputWindow
from PyQt6.QtWidgets import QApplication
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)
    first_window = LinkInputWindow()
    app.exec()


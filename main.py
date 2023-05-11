from qt.global_window import LinkInputWindow
from PyQt6.QtWidgets import QApplication
import sys
from DB.history_matches import DataBase

if __name__ == '__main__':
	DataBase().check_match()
	APP = QApplication(sys.argv)
	window = LinkInputWindow()
	APP.exec()

#!/bin/env python3
# coding: utf-8

from PyQt6 import uic

import sys

from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QProgressBar, QVBoxLayout, QDialog, QApplication, QWidget
from multi_threading.q_thread_worker import ThreadLogic


class WindowPB(QDialog):
	def __init__(self, window):
		super().__init__(window)
		self.window = window
		self.setWindowIcon(QIcon('qt/icons/data-analytics-CSGO.ico'))
		self.setWindowTitle("Загрузка")
		self.setGeometry(500, 200, 300, 100)
		vbox = QVBoxLayout()
		self.progressbar = QProgressBar()
		self.progressbar.setMaximum(0)
		self.progressbar.setMaximum(100)
		self.progressbar.setTextVisible(False)
		self.progressbar.setStyleSheet("QProgre"
		                               "ssBar {border: 2px solid grey;border-radius:2px;padding:1px}"
		                               "QProgressBar::chunk {background:rgb(255, 255, 255)}")
		vbox.addWidget(self.progressbar)
		self.setLayout(vbox)

	def upp_value(self, value):
		self.progressbar.setValue(value)


class LinkInputWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.work_in_thread = None
		self.window = uic.loadUi('qt/uis/first_window.ui', self)
		self.progressbar_window = WindowPB(self.window)
		self.window.setWindowIcon(QIcon('qt/icons/data-analytics-CSGO.ico'))
		self.window.setWindowTitle('CS-GO Analytics')
		self.window.next_button.clicked.connect(self.take_link)
		self.window.show()

	def take_link(self):
		link = self.input_link.text()
		if link == '' or link.find('https://') != 0:
			error = QMessageBox()
			error.setWindowTitle('Ошибка ввода ссылки')
			error.setText('Ссылка на сайт указанна неверно.')
			error.setIcon(QMessageBox.Icon.Warning)
			error.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
			error.exec()
		else:
			try:
				self.window.hide()
				self.progressbar_window.show()
				self.start_work_in_site(link)
			except ValueError:
				error = QMessageBox()
				error.setWindowTitle('Ошибка работы с матчем')
				error.setText(
					'1.Матч уже начался, либо близок к началу.\n2.Ссылка на матч указана неверно.\n3.Одна из команд ещё не определена.')
				error.setIcon(QMessageBox.Icon.Warning)
				error.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
				error.exec()

	def start_work_in_site(self, link):
		self.work_in_thread = ThreadLogic(link)
		self.work_in_thread.progress_bar_signal.connect(self.progressbar_window.upp_value)
		self.work_in_thread.finished_signal.connect(self.after_finish)
		self.work_in_thread.start()

	def after_finish(self):
		self.close()
		self.progressbar_window.close()
		UI()
		#open_ui()


class UI(QMainWindow):
	def __init__(self):
		super().__init__()
		self.window = uic.loadUi('qt/uis/main_window.ui', self)
		self.window.setWindowIcon(QIcon('qt/icons/data-analytics-CSGO.ico'))
		self.set_basis_info_tab()
		self.window.show()

	def set_basis_info_tab(self):
		self.window.png_team_one.setPixmap(QPixmap('qt/icons/data-analytics-CSGO.ico'))
		self.window.png_team_one.adjustSize()
		self.window.png_team_two.setPixmap(QPixmap('qt/icons/data-analytics-CSGO.ico'))
		self.window.png_team_two.adjustSize()

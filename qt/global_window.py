#!/bin/env python3
# coding: utf-8
import time
import threading

from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import QMainWindow, QMessageBox, QProgressBar, QVBoxLayout, QDialog
from parsing.work_in_site import WorkInSite
from analytics.data_analysis import DataAnalysis


class ThreadLogic(QThread):
	progress_bar_signal = pyqtSignal(int)

	def __init__(self, link):
		super().__init__()
		self.link = link

	def run(self):
		wk = WorkInSite(self.link)
		name1, name2, history_score_dict, best_of_number, coefficient_dict, dict_old_scores, win_1, win_2 = wk.ret_all_value()
		self.progress_bar_signal.emit(20)
		dt = DataAnalysis(name1, name2, history_score_dict, best_of_number, coefficient_dict, dict_old_scores, win_1, win_2)
		self.progress_bar_signal.emit(30)


class WindowPB(QDialog):
	def __init__(self, window):
		super().__init__(window)
		self.val = 0
		self.window = window
		self.title = "PyQt6 ProgressBar"
		self.top = 200
		self.left = 500
		self.width = 300
		self.height = 100
		self.setWindowIcon(QIcon("icon.png"))
		self.setWindowTitle(self.title)
		self.setGeometry(self.left, self.top, self.width, self.height)
		vbox = QVBoxLayout()
		self.progressbar = QProgressBar()
		self.progressbar.setMaximum(100)
		self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
		                               "QProgressBar::chunk {background:yellow}")
		vbox.addWidget(self.progressbar)
		self.setLayout(vbox)

	def upp_value(self, value):
		self.progressbar.setValue(value)


class Window(QMainWindow):
	def __init__(self):
		super().__init__()

	def connect_to_ui_file(self, file: str):
		return uic.loadUi(file, self)  # Load the .ui file


class LinkInputWindow(Window):
	def __init__(self):
		super().__init__()
		self.work_in_thread = None
		self.window = self.connect_to_ui_file('qt/uis/first_window.ui')
		self.progressbar_window = WindowPB(self.window)
		self.window.setWindowIcon(QIcon('icons/data-analytics-CSGO.ico'))
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
				print('qqqq')
				self.start_work_in_site(link)
				print('sss')
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
		self.work_in_thread.start()


class UI(Window):
	def __init__(self):
		super().__init__()
		self.connect_to_ui_file('qt/uis/main_window.ui')
		self.setWindowIcon(QIcon('icons/data-analytics-CSGO.ico'))
		self.show()

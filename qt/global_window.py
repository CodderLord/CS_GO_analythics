#!/bin/env python3
# coding: utf-8
import time

from PyQt6 import uic
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QThread, QObject, pyqtSlot, pyqtSignal
from PyQt6.QtWidgets import QMainWindow, QMessageBox
from parsing.work_in_site import WorkInSite


class BasisThread(QObject):
	@pyqtSlot(int)
	def run(self, n):
		ProgressBarWindow()


class Window(QMainWindow):
	def __init__(self):
		super().__init__()

	def connect_to_ui_file(self, file: str):
		uic.loadUi(file, self)  # Load the .ui file


class ProgressBarWindow(Window):
	def __init__(self):
		super().__init__()
		self.connect_to_ui_file('qt/second_window.ui')
		self.__progress_bar_value = 0
		self.show()


class LinkInputWindow(Window):
	work_requested = pyqtSignal(int)

	def __init__(self):
		super().__init__()
		self.connect_to_ui_file('qt/first_window.ui')
		self.next_button.clicked.connect(self.on_click_parse_link)
		self.worker = BasisThread()
		self.worker_thread = QThread()
		self.work_requested.connect(self.worker.run)
		self.worker.moveToThread(self.worker_thread)
		self.worker_thread.start()
		self.show()

	def on_click_parse_link(self):
		self.take_link()

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
				#self.destroy()
				#self.work_requested.emit(5)
				#WorkInSite(link)
				pass
			except ValueError:
				error = QMessageBox()
				error.setWindowTitle('Ошибка работы с матчем')
				error.setText(
					'1.Матч уже начался, либо близок к началу.\n2.Ссылка на матч указана неверно.\n3.Одна из команд ещё не определена.')
				error.setIcon(QMessageBox.Icon.Warning)
				error.setStandardButtons(QMessageBox.StandardButton.Ok | QMessageBox.StandardButton.Cancel)
				error.exec()


class UI(Window):

	def __init__(self):
		super().__init__()
		self.connect_to_ui_file('qt/first_window.ui')
		self.setWindowIcon(QIcon('icons/data-analytics-CSGO.ico'))
		self.show()


from PyQt6.QtCore import pyqtSignal, QThread
from parsing.work_in_site import WorkInSite
from analytics.data_analysis import DataAnalysis
from diagrams.diagrams import DiagramsCreate


class ThreadLogic(QThread):
	progress_bar_signal = pyqtSignal(int)
	finished_signal = pyqtSignal(str)
	error_signal = pyqtSignal()

	def __init__(self, link):
		super().__init__()
		self.link = link

	def run(self):
		self.progress_bar_signal.emit(10)
		print('start')
		wk = WorkInSite(self.link)
		print('wk end')
		self.progress_bar_signal.emit(15)
		path = wk.ret_path()
		print('path end')
		self.progress_bar_signal.emit(20)
		DataAnalysis(path)
		print('DataAnalysis end')
		self.progress_bar_signal.emit(30)
		DiagramsCreate(path, self.progress_bar_signal)
		print('DiagramsCreate end')
		self.progress_bar_signal.emit(95)
		self.finished_signal.emit(path)

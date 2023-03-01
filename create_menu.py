import tkinter as tk
from tkinter.ttk import Progressbar
import tkinter.messagebox as mb
from tkinter import Label
from work_in_site import WorkInSite
import webbrowser


class App(tk.Tk):
	def __init__(self):
		super().__init__()
		self.btn_next = tk.Button(self, text="Начали", command=self.click_further)
		self.btn_more = tk.Button(self, text="Подробнее", command=self.click_more)
		self.btn_open = tk.Button(self, text="Сайт", command=lambda: webbrowser.open('https://game-tournaments.com/csgo'))
		self.label = Label(self, text="Введите рабочую ссылку на матч")
		# disable resizing
		self.resizable(False, False)
		self.title('i-Analytics')
		# create label from
		self.iconbitmap('data-analytics-CSGO.ico')
		# -150 == my center screen
		self.geometry(f'+{self.winfo_screenwidth()//2-150}+{self.winfo_screenheight()//2-150}')
		self.name = tk.Entry(self)
		# create label, button to coordinate
		self.label.pack(padx=20, pady=20)
		self.btn_open.pack()
		self.name.pack(padx=20, pady=20)
		self.btn_next.pack(padx=5, pady=5)
		self.btn_more.pack(padx=5, pady=5)

	def click_further(self):
		url = self.name.get()
		if url == '' or url.find('https://') != 0:
			mb.showerror('Ошибка', 'Нужно указать рабочую ссылку на матч.')
		else:
			self.next_window(url)

	def next_window(self, url):
		self.label.configure(text='Началась обработка сайта')
		self.btn_more.destroy()
		self.btn_next.destroy()
		self.name.destroy()
		progressbar = Progressbar(self, length=300, style='black.Horizontal.TProgressbar', mode="indeterminate")
		progressbar.pack(padx=5, pady=5)
		progressbar.start(10)
		btn_cancel = tk.Button(self, text="Отмена", command=lambda: self.destroy())
		btn_cancel.pack(padx=5, pady=5)
		try:
			WorkInSite(url)
		except ValueError:
			mb.showerror('Ошибка', '1.Матч уже начался, либо близок к началу.\n2.Ссылка на матч указана неверно.\n3.Одна из команд ещё не определена.')
			App.destroy(self)
			new_app = App()
			new_app.mainloop()

	@staticmethod
	def click_more():
		mb.showinfo('Подробности', 'Нужно указать рабочую ссылку на матч в виде "https://game-tournaments.com/ru/csgo/some"\nМатч по ссылке не должен быть начат/закончен.\nИсходный сайт должен быть на русском языке.\nЕсли не работают горячие клавиши - измените язык ввода на ENG')
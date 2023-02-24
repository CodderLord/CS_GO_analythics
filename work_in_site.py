import requests
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from help_file import translate_to_datatime, NOW_time


software_names = [SoftwareName.CHROME.value]
operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
DOM = 'https://game-tournaments.com'


class Soup(BeautifulSoup):
	def __init__(self, url):
		super().__init__()
		self.url = url
		self.bs = BeautifulSoup


class Connect(Soup):
	def __init__(self, url):
		super().__init__(url)
		self.requests = requests
		self.user_agent = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
		self.redy_soup = self.try_to_connect(url)

	def try_to_connect(self, url):
		html_url = self.requests.get(url, headers={'user-agent': f'{self.user_agent.get_random_user_agent()}'})
		# check status code
		if html_url.status_code == 200:
			print('Status code is o`k :)')
			# HTML code ready to parse
			return self.connect_site(html_url)
		else:
			print('Status code is NOT o`k')
			raise ValueError

	def connect_site(self, html_url):
		redy_soup = self.bs(html_url.text, 'html.parser')
		return redy_soup


class WorkInSite(Connect):
	def __init__(self, url):
		super().__init__(url)
		self.title = self.redy_soup.find(class_='match-header').find('h1').text.strip().replace('Матч ', '')
		self.name_1, self.name_2 = self.title.split(' vs ')
		if self.name_1 == 'TBD' or self.name_2 == 'TBD':
			raise ValueError
		self.check_game()
		self.score_dict = self.find_history_tvt()
		self.best_of_number = self.find_best_of()
		self.coefficient_dict = self.find_coefficient_on_bookmaker()
		self.dict_old_scores = self.find_form_teams()
		self.win_1, self.win_2 = self.find_experience()
		self.same_team_list_1 = []
		self.same_team_list_2 = []

	def check_game(self):
		"""
		checking the start of the game used modul datatime
		:return:Value error if this game is start or end
		"""
		time_date, time = self.redy_soup.find(class_='stage-time').find('time').get('datetime').split('T')
		year, month, day = time_date.split('-')
		hour, minute = time.split(":")
		# hour - 1(website operation specification)
		time_g = translate_to_datatime(year=int(year), month=int(month), day=int(day), hour=int(hour)+1, minute=int(minute))
		if time_g < NOW_time:
			print('This game is played')
			raise ValueError

	def find_history_tvt(self):
		"""
		def for find history team vs team
		:return: dict with account and name OR None if no history
		"""
		score_dict = {self.name_1: 0, self.name_2: 0}
		try:
			history_url = DOM + str(self.redy_soup.find(class_='btn btn-xs btn-default pull-right').get('href'))
		except AttributeError:
			return
		history_soup = self.try_to_connect(history_url)
		tr_all = history_soup.find(class_='table-responsive').find_all('tr')
		for i in tr_all:
			span = i.find_all_next('span')
			score_list = span[2].text.strip().split('\n')
			name_1 = span[1].text.strip().replace('\n', '')
			name_2 = span[7].text.strip().replace('\n', '')
			try:
				coefficient_old_1, score, coefficient_old_2 = score_list[0], score_list[2], score_list[4]
			except IndexError:
				score = score_list[0]
			score_1, score_2 = score.split(' : ')
			date = i.find_next(class_='sct').get('data-time').split(' ')[0].split('-')
			year, month, day = date[0], date[1], date[2]
			date_time = translate_to_datatime(year=int(year), month=int(month), day=int(day))
			delta = date_time - NOW_time
			# if the event happened less than 3 months ago(89 days)
			if delta.days >= -89:
				score_dict[name_1] += int(score_1)
				score_dict[name_2] += int(score_2)
		return score_dict

	def find_best_of(self):
		"""
		how many game (bo1-bo2-bo3-bo5)
		:return: int
		"""
		return self.redy_soup.find(class_='stage-time').text.split(', ')[-1].split(' ')[-1]

	def find_coefficient_on_bookmaker(self):
		"""
		which coefficient on open bookmakers
		:return:dict_coefficient
		"""
		dict_coefficient = {self.name_1: 0.0}
		box = self.redy_soup.find(class_='box kfbox clearfix')
		row = box.find_all(class_='row2 clearfix rowkoef')
		for i in row:
			first_team = i.find_next(class_='text-right').text
			first_coefficient, second_coefficient = i.find_next(class_='text-center').text.strip().replace('\xa0', '').split('–')
			try:
				dict_coefficient[first_team] = (dict_coefficient[first_team] + float(first_coefficient))/2 \
					if dict_coefficient[first_team] != 0.0 else float(first_coefficient)
			except KeyError:
				dict_coefficient[self.name_1] = (dict_coefficient[self.name_1] + float(second_coefficient))/2 \
					if dict_coefficient[self.name_1] != 0.0 else float(second_coefficient)
		return dict_coefficient

	def find_form_teams(self):
		"""
		which form at team
		:return:dict_scores
		"""
		dict_scores = {self.name_1: 0, self.name_2: 0}
		href_1, href_2 = self.redy_soup.find_all(class_='mteamname')
		href_1 = DOM + href_1.find('a').get('href')
		href_2 = DOM + href_2.find('a').get('href')
		ready_soup_url_1 = self.try_to_connect(href_1)
		box_before = ready_soup_url_1.find_all(class_='box clearfix')[1]
		tr_all_url_1 = box_before.find_all('tr')
		for i in tr_all_url_1:
			name_1_1 = i.find_next(class_='teamname c1').text.strip()
			name_1_2 = i.find_next(class_='teamname c2').text.strip()
			year_1, month_1, day_1 = i.find_next(class_='sct').get('data-time').split(' ')[0].split('-')
			delta_1 = translate_to_datatime(year=int(year_1), month=int(month_1), day=int(day_1)) - NOW_time
			if delta_1.days >= -60:
				score_1, score_2 = i.find_next(class_='vs').find_next('span').get('data-score').split(' : ')
				try:
					dict_scores[name_1_1] += int(score_1.replace('*', ''))
				except KeyError:
					dict_scores[name_1_2] += int(score_2.replace('*', ''))
		# ----------------------
		ready_soup_url_2 = self.try_to_connect(href_2)
		box_before = ready_soup_url_2.find_all(class_='box clearfix')[1]
		tr_all_url_2 = box_before.find_all('tr')
		for i in tr_all_url_2:
			name_2_1 = i.find_next(class_='teamname c1').text.strip()
			name_2_2 = i.find_next(class_='teamname c2').text.strip()
			year_2, month_2, day_2 = i.find_next(class_='sct').get('data-time').split(' ')[0].split('-')
			delta_2 = translate_to_datatime(year=int(year_2), month=int(month_2), day=int(day_2)) - NOW_time
			if delta_2.days >= -60:
				score_1, score_2 = i.find_next(class_='vs').find_next('span').get('data-score').split(' : ')
				try:
					dict_scores[name_2_1] += int(score_1.replace('*', ''))
				except KeyError:
					dict_scores[name_2_2] += int(score_2.replace('*', ''))
		return dict_scores

	def find_experience(self):
		"""
		experience teams(col. games)
		:return: 2 int
		"""
		href_1, href_2 = self.redy_soup.find_all(class_='mteamname')
		href_1 = DOM + href_1.find('a').get('href')
		ready_soup_url_1 = self.try_to_connect(href_1)
		try:
			winn_1 = ready_soup_url_1.find_all(class_='col col-xs-3')[-1].text.split(' ')[1]
		except IndexError:
			winn_1 = 0
		# -------------------------
		href_2 = DOM + href_2.find('a').get('href')
		ready_soup_url_2 = self.try_to_connect(href_2)
		try:
			winn_2 = ready_soup_url_2.find_all(class_='col col-xs-3')[-1].text.split(' ')[1]
		except IndexError:
			winn_2 = 0
		return winn_1, winn_2

	def find_same_team(self, tr_all):
		"""
		get tr_all
		find one more team which is in the history of games team here and there
		:return:
		"""
		main_list = []
		for i in tr_all:
			name_1 = i.find_next(class_='teamname c1').text.strip()
			name_2 = i.find_next(class_='teamname c2').text.strip()

		def add_same_team_to_dict():
			pass

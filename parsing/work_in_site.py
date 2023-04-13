import json

import requests

from bs4 import BeautifulSoup


from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem


from parsing.help_file import translate_to_datatime, NOW_time, first_name_dict, second_name_dict, first_same_name_dict,\
	second_same_name_dict


from os import makedirs, path


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
			# HTML code ready to parse
			return self.connect_site(html_url)
		else:
			raise ValueError

	def connect_site(self, html_url):
		redy_soup = self.bs(html_url.text, 'html.parser')
		return redy_soup


def create_directory_team(name_1, name_2):
	new_path = r'team_info\{}_vs_{}'.format(name_1.replace(' ', ''), name_2.replace(' ', ''))
	if not path.exists('team_info'):
		makedirs('team_info')
	if not path.exists(new_path):
		makedirs(new_path)
	return new_path


def download_img(url, name, path_main):
	p = requests.get(url)
	try:
		try_to_open = open(r"{}\{}.jpg".format(path_main, name))
		try_to_open.close()
	except FileNotFoundError:
		out = open(r"{}\{}.jpg".format(path_main, name), "wb")
		out.write(p.content)
		out.close()


class WorkInSite(Connect):
	def __init__(self, url):
		super().__init__(url)
		self.team_info_dict = {}
		self.title = self.redy_soup.find(class_='match-header').find('h1').text.strip().replace('Матч ', '')
		self.name_1, self.name_2 = self.title.split(' vs ')
		self.img_url_1, self.img_url_2 = self.find_img()
		self.path = create_directory_team(self.name_1, self.name_2)
		download_img(self.img_url_1, self.name_1, self.path)
		download_img(self.img_url_2, self.name_2, self.path)
		if self.name_1 == 'TBD' or self.name_2 == 'TBD':
			raise ValueError
		self.check_game()
		self.history_score_dict, self.trend_score_dict, self.time_zone_history_list = self.find_history_tvt(self.name_1, self.name_2)
		self.best_of_number = self.find_best_of()
		self.coefficient_dict = self.find_coefficient_on_bookmaker()
		self.dict_old_scores, self.list_old_scores_one, self.list_old_scores_two, self.list_timezone_old_score_one, self.list_timezone_old_score_two, self.team_one_old_scores_win, self.team_one_old_scores_lose, self.team_two_old_scores_win, self.team_two_old_scores_lose = self.find_form_teams()
		self.win_1, self.win_2, self.percent_1, self.percent_2 = self.find_experience()  # number of team wins
		self.find_same_teams()  # first_same_dict, second_same_dict
		try:
			self.team_info_dict_fill()
		except Exception as err:
			print(err)

	def ret_path(self):
		return self.path

	def team_info_dict_fill(self):
		self.team_info_dict['title'] = self.title if not None else 0
		self.team_info_dict['name_1'] = self.name_1 if not None else 0
		self.team_info_dict['name_2'] = self.name_2 if not None else 0
		self.team_info_dict['img_url_1'] = self.img_url_1 if not None else 0
		self.team_info_dict['img_url_2'] = self.img_url_2 if not None else 0
		self.team_info_dict['path_on_disc'] = self.path if not None else 0
		self.team_info_dict['history_score_dict'] = self.history_score_dict if not None else 0
		self.team_info_dict['history_trend_dict'] = self.trend_score_dict if not None else 0
		self.team_info_dict['history_time_zone_list'] = self.time_zone_history_list if not None else 0
		self.team_info_dict['best_of_number'] = self.best_of_number if not None else 0
		self.team_info_dict['coefficient_dict'] = self.coefficient_dict if not None else 0
		self.team_info_dict['dict_old_scores'] = self.dict_old_scores if not None else 0
		self.team_info_dict['win_1'] = self.win_1 if not None else 0
		self.team_info_dict['win_2'] = self.win_2 if not None else 0
		self.team_info_dict['percent_win_1'] = self.percent_1 if not None else 0
		self.team_info_dict['percent_win_2'] = self.percent_2 if not None else 0
		self.team_info_dict['list_old_scores_one'] = self.list_old_scores_one if not None else 0
		self.team_info_dict['list_old_scores_two'] = self.list_old_scores_two if not None else 0
		self.team_info_dict['team_one_old_scores_win'] = self.team_one_old_scores_win if not None else 0
		self.team_info_dict['team_one_old_scores_lose'] = self.team_one_old_scores_lose if not None else 0
		self.team_info_dict['team_two_old_scores_win'] = self.team_two_old_scores_win if not None else 0
		self.team_info_dict['team_two_old_scores_lose'] = self.team_two_old_scores_lose if not None else 0
		self.team_info_dict['list_timezone_old_score_one'] = self.list_timezone_old_score_one if not None else 0
		self.team_info_dict['list_timezone_old_score_two'] = self.list_timezone_old_score_two if not None else 0
		self.save_parse_info_on_js()

	def save_parse_info_on_js(self):
		with open(f"{self.path}/config", "w") as fh:
			json.dump(self.team_info_dict, fh)

	def check_game(self):
		"""
		checking the start of the game used modul datatime
		:return:Value error if this game is start or end
		"""
		time_date, time = self.redy_soup.find(class_='stage-time').find('time').get('datetime').split('T')
		year, month, day = time_date.split('-')
		hour, minute = time.split(":")
		# hour + 2(website operation specification)
		time_g = translate_to_datatime(year=int(year), month=int(month), day=int(day), hour=int(hour)+2, minute=int(minute))
		if time_g < NOW_time:
			print('This game is played')
			raise ValueError

	def find_img(self):
		url_img_1 = DOM + self.redy_soup.find(class_='mop1').find(class_='mteamlogo').find('img').get('src')
		url_img_2 = DOM + self.redy_soup.find(class_='mop2').find(class_='mteamlogo').find('img').get('src')
		return url_img_1, url_img_2

	def find_history_tvt(self, name_1, name_2):
		"""
		def for find history team vs team
		:return: dict with account and name OR None if no history
		"""
		score_dict = {self.name_1: 0, self.name_2: 0}
		trend_score_dict = {self.name_1: [], self.name_2: []}
		time_zone_list = []
		try:
			history_url = DOM + str(self.redy_soup.find(class_='btn btn-xs btn-default pull-right').get('href'))
		except AttributeError:
			return {f'{name_1}': [0], f'{name_2}': [0]},\
				{f'{name_1}': [0], f'{name_2}': [0]}, ['0']
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
			time_zone_list.append(f'{month}\n{year[-2]}{year[-1]}')
			date_time = translate_to_datatime(year=int(year), month=int(month), day=int(day))
			delta = date_time - NOW_time
			# if the event happened less than 3 months ago(89 days)
			trend_score_dict[name_1].append(int(score_1))
			trend_score_dict[name_2].append(int(score_2))
			if delta.days >= -89:
				score_dict[name_1] += int(score_1)
				score_dict[name_2] += int(score_2)
		return score_dict, trend_score_dict, time_zone_list

	def find_best_of(self):
		"""
		how many game (bo1-bo2-bo3-bo5)
		:return: int
		"""
		return self.redy_soup.find(class_='stage-time').text.split(', ')[-1].split(' ')[-1].strip()

	def find_coefficient_on_bookmaker(self):
		"""
		which coefficient on open bookmakers
		:return:dict_coefficient
		"""
		dict_coefficient = {self.name_1: 0.0, self.name_2: 0.0}
		box = self.redy_soup.find(class_='box kfbox clearfix')
		try:
			row = box.find_all(class_='row2 clearfix rowkoef')
		except AttributeError:
			return dict_coefficient
		for i in row:
			first_team = i.find_next(class_='text-right').text
			second_team = i.find_all_next('td')[2].text
			first_coefficient, second_coefficient = i.find_next(class_='text-center').text.strip().replace('\xa0', '').split('–')
			dict_coefficient[first_team] = (dict_coefficient[first_team] + float(first_coefficient))/2 \
				if dict_coefficient[first_team] != 0.0 else float(first_coefficient)
			dict_coefficient[second_team] = (dict_coefficient[second_team] + float(second_coefficient))/2 \
				if dict_coefficient[second_team] != 0.0 else float(second_coefficient)
		return dict_coefficient

	def find_form_teams(self):
		"""
		which form at team
		:return:dict_scores
		"""
		team_one_old_scores = []
		team_one_old_scores_time_zone = []
		team_one_old_scores_win = []
		team_one_old_scores_lose = []
		team_two_old_scores = []
		team_two_old_scores_time_zone = []
		team_two_old_scores_win = []
		team_two_old_scores_lose = []
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
			if delta_1.days >= -90:
				score_1, score_2 = i.find_next(class_='vs').find_next('span').get('data-score').split(' : ')
				score_1, score_2 = int(score_1.replace('*', '')), int(score_2.replace('*', ''))
				self.add_names_to_dict(1, name_1_1, name_1_2, score_1, score_2)
				try:
					dict_scores[name_1_1] += score_1
					team_one_old_scores.append(score_1)
					if score_1 > score_2:
						team_one_old_scores_win.append(score_1)
					else:
						team_one_old_scores_lose.append(score_2)
				except KeyError:
					dict_scores[name_1_2] += score_2
					team_one_old_scores.append(score_2)
					if score_2 > score_1:
						team_one_old_scores_win.append(score_2)
					else:
						team_one_old_scores_lose.append(score_1)
				team_one_old_scores_time_zone.append(f'{month_1}\n{year_1[-2]}{year_1[-1]}')
		# ----------------------
		ready_soup_url_2 = self.try_to_connect(href_2)
		box_before = ready_soup_url_2.find_all(class_='box clearfix')[1]
		tr_all_url_2 = box_before.find_all('tr')
		for i in tr_all_url_2:
			name_2_1 = i.find_next(class_='teamname c1').text.strip()
			name_2_2 = i.find_next(class_='teamname c2').text.strip()
			year_2, month_2, day_2 = i.find_next(class_='sct').get('data-time').split(' ')[0].split('-')
			delta_2 = translate_to_datatime(year=int(year_2), month=int(month_2), day=int(day_2)) - NOW_time
			if delta_2.days >= -90:
				score_1, score_2 = i.find_next(class_='vs').find_next('span').get('data-score').split(' : ')
				score_1, score_2 = int(score_1.replace('*', '')), int(score_2.replace('*', ''))
				self.add_names_to_dict(2, name_2_1, name_2_2, score_1, score_2)
				try:
					dict_scores[name_2_1] += score_1
					team_two_old_scores.append(score_1)
					if score_1 > score_2:
						team_two_old_scores_win.append(score_1)
					else:
						team_two_old_scores_lose.append(score_2)
				except KeyError:
					dict_scores[name_2_2] += score_2
					team_two_old_scores.append(score_2)
					if score_2 > score_1:
						team_two_old_scores_win.append(score_2)
					else:
						team_two_old_scores_lose.append(score_1)
				team_two_old_scores_time_zone.append(f'{month_2}\n{year_2[-2]}{year_2[-1]}')
		return dict_scores, team_one_old_scores, team_two_old_scores, team_one_old_scores_time_zone, team_two_old_scores_time_zone, team_one_old_scores_win, team_one_old_scores_lose, team_two_old_scores_win, team_two_old_scores_lose

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
			percent_1 = ready_soup_url_1.find_all(class_='col col-xs-3')[-1].text.split(' ')[-1]
		except IndexError:
			winn_1 = 0
			percent_1 = 0
		# -------------------------
		href_2 = DOM + href_2.find('a').get('href')
		ready_soup_url_2 = self.try_to_connect(href_2)
		try:
			winn_2 = ready_soup_url_2.find_all(class_='col col-xs-3')[-1].text.split(' ')[1]
			percent_2 = ready_soup_url_2.find_all(class_='col col-xs-3')[-1].text.split(' ')[-1]
		except IndexError:
			winn_2 = 0
			percent_2 = 0
		return winn_1, winn_2, percent_1, percent_2

	@staticmethod
	def find_same_teams():
		"""
		filterer dicts to find same teams on first_name_dict and second_name_dict
		"""
		first_list = first_name_dict.keys()
		for i in first_list:
			try:
				__try_to_err = second_name_dict[i]  # try to find name from list first to dict second else continue
				# first number score its col. maps which win self.name_1(if first) or self.name_2(if second)
				first_same_name_dict[i] = first_name_dict[i]
				second_same_name_dict[i] = second_name_dict[i]
			except KeyError:
				continue

	def add_names_to_dict(self, main_naim_team: int, pos_firs: str, pos_second, score_1: int, score_2: int):
		"""
		add all teams and score(map) to dict
		"""
		if pos_firs != self.name_1 and pos_firs != self.name_2:
			if main_naim_team == 1:
				first_name_dict[pos_firs] = f'{score_1}-{score_2}'
			if main_naim_team == 2:
				second_name_dict[pos_firs] = f'{score_1}-{score_2}'
		if pos_second != self.name_1 and pos_second != self.name_2:
			if main_naim_team == 1:
				first_name_dict[pos_firs] = f'{score_2}-{score_1}'
			if main_naim_team == 2:
				second_name_dict[pos_firs] = f'{score_2}-{score_1}'

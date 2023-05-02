import time

import matplotlib.pyplot as plt
import matplotlib.ticker
from parsing.help_file import load_config_json

import numpy as np
matplotlib.use('QtAgg')


class DiagramsCreate:
	def __init__(self, path, signal):
		self.signal = signal
		self.path = path
		self.team_info_dict = load_config_json(self.path)
		# ratio history
		self.create_ratio_diagram(self.team_info_dict['percent_history_one'], self.team_info_dict['percent_history_two'], 'history_graphics', 'Соотношение истории игр команд')
		self.signal.emit(35)
		time.sleep(0.3)
		# trend history
		self.create_trend_diagram((self.team_info_dict['history_trend_dict'])[self.team_info_dict['name_1']],(self.team_info_dict['history_trend_dict'])[self.team_info_dict['name_2']], self.team_info_dict['history_time_zone_list'], 'history_trend_graphics', 'Тренд истории игр')
		self.signal.emit(40)
		time.sleep(0.3)
		# ratio coefficient
		self.create_ratio_diagram(self.team_info_dict['percent_coefficient_one'], self.team_info_dict['percent_coefficient_two'], 'coefficient_graphics', 'Соотношения коефициентов команд')
		self.signal.emit(45)
		time.sleep(0.3)
		# ratio experience (not ready)
		self.create_ratio_diagram(self.team_info_dict['percent_experience_1'], self.team_info_dict['percent_experience_2'], 'experience_graphics', 'Соотношение общего опыта команд\nза всё время')
		self.signal.emit(50)
		time.sleep(0.3)
		# trend form team one
		self.create_trend_diagram(self.team_info_dict['list_old_scores_one'], [], self.team_info_dict['list_timezone_old_score_one'], 'old_scores_trend_graphics_one', f'Тренд истории игр команды {self.team_info_dict["name_1"]}')
		self.signal.emit(55)
		time.sleep(0.3)
		# trend form team two
		self.create_trend_diagram([], self.team_info_dict['list_old_scores_two'], self.team_info_dict['list_timezone_old_score_two'], 'old_scores_trend_graphics_two', f'Тренд истории игр команды {self.team_info_dict["name_2"]}')
		self.signal.emit(60)
		time.sleep(0.3)
		# ratio form
		self.create_ratio_diagram(self.team_info_dict['percent_form_one'], self.team_info_dict['percent_form_two'], 'form_graphics', 'Соотношение истории игр команд')
		self.signal.emit(65)
		time.sleep(0.3)
		# ratio winning form
		self.create_ratio_diagram(self.team_info_dict['percent_team_one_old_scores_win'], self.team_info_dict['percent_team_two_old_scores_win'], 'old_scores_ratio_graphics_win', 'Соотношение форм команд\n(ПОБЕДЫ)')
		self.signal.emit(70)
		time.sleep(0.3)
		# ratio losing form
		self.create_ratio_diagram(self.team_info_dict['percent_team_two_old_scores_lose'], self.team_info_dict['percent_team_one_old_scores_lose'], 'old_scores_ratio_graphics_lose', 'Соотношение форм команд\n(ПОРАЖЕНИЯ)')
		self.signal.emit(75)
		time.sleep(0.3)
		# ratio same teams (WIN)
		(first_win, second_win), (first_lose, second_lose) = self.team_info_dict['same_teams_scores']
		self.create_ratio_diagram(first_win, second_win, 'same_win_graphics', 'Соотношение побед команд \nв игре с одинаковыми командами')
		self.signal.emit(80)
		time.sleep(0.3)
		# ratio same teams (LOSE)
		self.create_ratio_diagram(first_lose, second_lose, 'same_lose_graphics', 'Соотношение поражений команд \nв игре с одинаковыми командами')
		self.signal.emit(85)
		time.sleep(0.3)
		# ratio exodus
		self.create_ratio_diagram(
			self.team_info_dict['first_exodus_percent'], self.team_info_dict['second_exodus_percent'], 'exodus_graphics', 'Исходный процент соотношения сил')
		time.sleep(0.3)
		# exodus diagram
		self.create_pentagon_diagram(
			first_values=self.team_info_dict['first_percents_for_pentagon'],
			second_values=self.team_info_dict['second_percents_for_pentagon'],
			name='pentagon_graphics',
			name_1=self.team_info_dict["name_1"],
			name_2=self.team_info_dict["name_2"])
		time.sleep(0.3)

	def create_ratio_diagram(self, percent_1, percent_2, name, title):
		fig, ax = plt.subplots()
		teams = [self.team_info_dict['name_1'], self.team_info_dict['name_2']]
		counts = [int(percent_1.replace('%', '')), int(percent_2.replace('%', ''))]
		bar_labels = [f'{self.team_info_dict["name_1"]}', f'{self.team_info_dict["name_2"]}']
		bar_colors = ['tab:red', 'tab:blue']
		ax.bar(teams, counts, label=bar_labels, color=bar_colors)
		ax.tick_params(labelcolor='white')
		fig.set_facecolor('#192B45')
		ax.set_facecolor('#132034')
		ax.set_ylabel('Соотношение(%)', color='white')
		ax.set_title(title, color='white')
		ax.legend(title='Цвет команд')
		plt.savefig(f'{self.path}/{name}.png')

	def create_trend_diagram(self, team_one_list, team_two_list, time_zone_list, name, title):
		team_one_list.reverse()
		team_two_list.reverse()
		time_zone_list.reverse()
		team_one = team_one_list
		team_two = team_two_list
		locator = matplotlib.ticker.FixedLocator([i for i in range(len(team_one if team_one != [] else team_two))])
		# plot the data
		fig = plt.figure()
		ax = fig.add_subplot()
		ax.xaxis.set_major_locator(locator)
		formatter = matplotlib.ticker.FixedFormatter(time_zone_list)
		ax.xaxis.set_major_formatter(formatter)
		ax.plot(team_one, color='tab:red')
		ax.plot(team_two, color='tab:blue')
		ax.tick_params(labelcolor='white')
		fig.set_facecolor('#192B45')
		ax.set_facecolor('xkcd:salmon')
		ax.tick_params(labelcolor='white')
		ax.set_facecolor('#132034')
		ax.set_title(f'{title}', color='white')
		ax.set_ylabel('Победы', color='white')
		ax.set_xlabel('')
		plt.savefig(f'{self.path}/{name}.png')

	def create_pentagon_diagram(self, name, first_values: list, second_values: list, name_1, name_2):
		n = 5
		angles = np.linspace(0, 2 * np.pi, n + 1)[:-1]
		fig = plt.figure()
		ax = fig.add_subplot(111, polar=True)
		ax.fill(angles, first_values, alpha=0.4, facecolor='red')  # first_values must have 5 values
		ax.fill(angles, second_values, alpha=0.4, facecolor='#004DFF')  # second_values must have 5 values
		ax.set_thetagrids(np.degrees(angles))
		ax.set_rlabel_position(0)
		ax.set_xticklabels(['Коеф.', 'Опыт', 'История', 'Форма', 'Третья сторона'], color='white')
		fig.set_facecolor('#192B45')
		ax.set_facecolor('#132034')
		ax.set_yticklabels([])
		ax.tick_params(pad=16)
		red_patch = plt.Rectangle((0, 0), 1, 1, fc="red", alpha=0.5)
		blue_patch = plt.Rectangle((0, 0), 1, 1, fc="#004DFF", alpha=0.5)
		legend = plt.legend([red_patch, blue_patch], [f'{name_1}', f'{name_2}'], loc='upper left', bbox_to_anchor=(-0.3, 1.13))
		legend.get_frame().set_facecolor('#132034')
		legend.get_frame().set_edgecolor('#132034')
		plt.setp(legend.get_texts(), color='white')
		plt.savefig(f'{self.path}/{name}.png')

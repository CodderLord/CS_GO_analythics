from parsing.help_file import first_same_name_dict, second_same_name_dict
from parsing.help_file import load_config_json
from DB.history_matches import DataBase
import json


def save_info_team_dict(path, team_info_dict):
	with open(f"{path}/config", "w+") as fh:
		json.dump(team_info_dict, fh)


class DataAnalysis:
	def __init__(self, path):
		self.dict_team_info = load_config_json(path)
		self.name_1: str = self.dict_team_info['name_1']
		self.name_2: str = self.dict_team_info['name_2']
		self.history_score_dict: dict or None = self.dict_team_info['history_score_dict']
		self.best_of_number: int = self.dict_team_info['best_of_number']  # number of best (bo1, bo2, bo3, bo5)
		self.coefficient_dict: dict = self.dict_team_info['coefficient_dict']  # coefficient on bookmakers
		# dict which have team names(self.name_1, self.name_2) and their scores
		self.dict_old_scores: dict = self.dict_team_info['dict_old_scores']
		self.win_1: int = int(str(self.dict_team_info['win_1']).replace('–', '0'))  # score of winning team
		self.win_2: int = int(str(self.dict_team_info['win_2']).replace('–', '0'))  # score of winning team
		try:
			self.percent_win_1 = int(str(self.dict_team_info['percent_win_1']).replace('%', ''))
		except ValueError:
			self.percent_win_1 = 0
		try:
			self.percent_win_2 = int(str(self.dict_team_info['percent_win_2']).replace('%', ''))
		except ValueError:
			self.percent_win_2 = 0
		self.percent_one_team_old_win = self.dict_team_info['team_one_old_scores_win']
		self.percent_one_team_old_lose = self.dict_team_info['team_one_old_scores_lose']
		self.percent_two_team_old_win = self.dict_team_info['team_two_old_scores_win']
		self.percent_two_team_old_lose = self.dict_team_info['team_two_old_scores_lose']
		self.first_same_teams: dict = first_same_name_dict  # dict which have names and scores same teams
		self.second_same_teams: dict = second_same_name_dict
		self.experience_1, self.experience_2 = self.calculate_all_wins()
		# -------------------------------------------
		self.dict_team_info['experience_1'], self.dict_team_info['experience_2'] = self.experience_1, self.experience_2
		self.dict_team_info['percent_experience_1'], self.dict_team_info['percent_experience_2'] =\
			self.calculate_percents_experience()
		self.dict_team_info['percent_history_one'], self.dict_team_info['percent_history_two'] =\
			self.calculate_history_score()
		self.dict_team_info['percent_coefficient_one'], self.dict_team_info['percent_coefficient_two'] =\
			self.calculate_coefficient()
		self.dict_team_info['percent_form_one'], self.dict_team_info['percent_form_two'] = self.calculate_old_scores()
		self.dict_team_info['percent_winning_one'], self.dict_team_info['percent_winning_two'] = self.calculate_winning()
		self.dict_team_info['percent_same_one'], self.dict_team_info['percent_same_two'] = self.calculate_same_teams()
		self.dict_team_info['percent_team_one_old_scores_win'], self.dict_team_info['percent_team_two_old_scores_win'] =\
			self.calculate_percents(sum(self.percent_one_team_old_win), sum(self.percent_two_team_old_win))
		self.dict_team_info['percent_team_one_old_scores_lose'], self.dict_team_info['percent_team_two_old_scores_lose'] =\
			self.calculate_percents(sum(self.percent_one_team_old_lose), sum(self.percent_two_team_old_lose))
		self.dict_team_info['first_same_dict'], self.dict_team_info['second_same_dict'] =\
			self.first_same_teams, self.second_same_teams
		self.first_lose_team_score, self.second_lose_team_score, self.first_win_team_score,\
			self.second_win_team_score = self.calculate_sames_scores()
		self.dict_team_info['team_one_win'], self.dict_team_info['team_two_win'],\
			self.dict_team_info['team_one_lose'], self.dict_team_info['team_two_lose'] =\
			self.first_win_team_score, self.second_win_team_score, self.first_lose_team_score, self.second_lose_team_score
		self.dict_team_info['same_teams_scores'] =\
			self.calculate_percents(self.first_win_team_score, self.second_win_team_score),\
			self.calculate_percents(self.second_lose_team_score, self.first_lose_team_score)
		(self.dict_team_info['first_exodus_percent'], self.dict_team_info['second_exodus_percent']),\
			self.dict_team_info['first_percents_for_pentagon'], self.dict_team_info['second_percents_for_pentagon'] = \
			self.exodus_percents()
		save_info_team_dict(self.dict_team_info['path_on_disc'], self.dict_team_info)
		try:
			self.add_info_to_data_base()
		except Exception as err:
			print(err)

	def calculate_percents_experience(self):
		percents_100 = self.experience_1 + self.experience_2
		percents_1 = percents_100/100
		percent_experience_1 = int(self.experience_1 / percents_1)
		percent_experience_2 = int(self.experience_2 / percents_1)
		return str(percent_experience_1)+'%', str(percent_experience_2)+'%'

	def calculate_all_wins(self):
		try:
			all_win_1 = int((self.win_1 / self.percent_win_1) * 100)
		except ZeroDivisionError:
			all_win_1 = 0
		try:
			all_win_2 = int((self.win_2 / self.percent_win_2) * 100)
		except ZeroDivisionError:
			all_win_2 = 0
		return all_win_1, all_win_2

	def calculate_history_score(self):
		"""
		assessment of past results of confrontation between teams and find percent winning
		"""
		try:
			score_1 = self.history_score_dict[self.name_1]
			score_2 = self.history_score_dict[self.name_2]
			percent_team_one, percent_team_two = self.calculate_percents(score_1, score_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		return percent_team_one, percent_team_two

	def calculate_coefficient(self):
		"""
		take into account the prediction of bookmakers
		"""
		try:
			coefficient_1 = self.coefficient_dict[self.name_1]
			coefficient_2 = self.coefficient_dict[self.name_2]
			percent_team_two, percent_team_one = self.calculate_percents(coefficient_1, coefficient_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		return percent_team_one, percent_team_two

	def calculate_old_scores(self):
		"""
		find 'form' team
		what form is the team in
		(ratio lose <-> win)
		"""
		try:
			old_score_1 = self.dict_old_scores[self.name_1]
			old_score_2 = self.dict_old_scores[self.name_2]
			percent_team_one, percent_team_two = self.calculate_percents(old_score_1, old_score_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		return percent_team_one, percent_team_two

	def calculate_winning(self):
		"""
		just calculate col. score winning team and find percent wining
		"""
		if self.win_1 != 0 and self.win_2 != 0:
			percent_team_one, percent_team_two = self.calculate_percents(self.win_1, self.win_2)
		else:
			percent_team_one = '50%'
			percent_team_two = '50%'
		return percent_team_one, percent_team_two

	def calculate_same_teams(self):
		"""
		takes dict with same teams(teams how was rival team_1 and team_2) and their scores for find percent winning
		"""
		first_same_score = 0
		second_same_score = 0
		list_names_first = self.first_same_teams.keys()
		for i in list_names_first:
			first_same_score += int(first_same_name_dict[i].split('-')[0])
			second_same_score += int(first_same_name_dict[i].split('-')[1])
			# ------------------------------------------------------------
			second_same_score += int(second_same_name_dict[i].split('-')[0])
			first_same_score += int(second_same_name_dict[i].split('-')[1])
		if first_same_score != 0 and second_same_score != 0:
			# if same teams not found
			percent_team_one, percent_team_two = self.calculate_percents(first_same_score, second_same_score)
		else:
			percent_team_one = '50%'
			percent_team_two = '50%'
		return percent_team_one, percent_team_two

	def calculate_sames_scores(self):
		names_teams = self.first_same_teams.keys()
		first_win_team_score: int = 0
		second_win_team_score: int = 0
		first_lose_team_score: int = 0
		second_lose_team_score: int = 0
		for i in names_teams:
			first_score_team_one = self.first_same_teams[i][0]
			first_score_team_two = self.first_same_teams[i][-1]
			second_score_team_one = self.second_same_teams[i][0]
			second_score_team_two = self.second_same_teams[i][-1]
			first_lose_team_score += int(first_score_team_one)
			second_lose_team_score += int(first_score_team_two)
			first_win_team_score += int(second_score_team_one)
			second_win_team_score += int(second_score_team_two)
		return first_lose_team_score, second_lose_team_score, first_win_team_score, second_win_team_score

	def exodus_percents(self):
		"""
		add all percents to one score
		:return: int, int - exodus percent
		"""
		first_percents = []
		second_percents = []
		# add percents to one team
		first_percents.append(int(self.dict_team_info['percent_coefficient_one'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_experience_1'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_history_one'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_form_one'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_same_one'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_win_1'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_winning_one'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_team_one_old_scores_win'].replace('%', '')))
		first_percents.append(int(self.dict_team_info['percent_team_two_old_scores_lose'].replace('%', '')))
		# add percents to two team
		second_percents.append(int(self.dict_team_info['percent_coefficient_two'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_experience_2'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_history_two'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_form_two'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_same_two'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_win_2'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_winning_two'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_team_two_old_scores_win'].replace('%', '')))
		second_percents.append(int(self.dict_team_info['percent_team_one_old_scores_lose'].replace('%', '')))
		first_exodus_percent = sum(first_percents)
		second_exodus_percent = sum(second_percents)
		return self.calculate_percents(first_exodus_percent, second_exodus_percent), first_percents[0:5], second_percents[0:5]
	
	def add_info_to_data_base(self):
		db = DataBase()
		title = self.dict_team_info['title']
		bo = self.dict_team_info['best_of_number']
		if int(self.dict_team_info['first_exodus_percent'].replace('%', '')) > \
			int(self.dict_team_info['second_exodus_percent'].replace('%', '')):
			result = 1
		elif int(self.dict_team_info['first_exodus_percent'].replace('%', '')) == \
			int(self.dict_team_info['second_exodus_percent'].replace('%', '')):
			result = 0
		elif int(self.dict_team_info['second_exodus_percent'].replace('%', '')) > \
			int(self.dict_team_info['first_exodus_percent'].replace('%', '')):
			result = -1  # if 1 first team will be winning; if 0 draw; if -1 second team will be winning
		else:
			result = None
		time_analytic = self.dict_team_info['now_time']
		db.commit_match(
			title_matches=title, bo_matches=bo, program_result=result,  time_analytic=time_analytic)

	@staticmethod
	def calculate_percents(score_1, score_2):
		"""
		func find percent from score
		:param score_1: first score int team(coefficient, score, etc.
		:param score_2: second score int team(coefficient, score, etc.
		:return: str: redy percents
		"""
		percent_100 = int(score_1) + int(score_2)
		percent_1 = percent_100 / 100
		try:
			percent_team_one = f"{int(score_1 / percent_1)}%"
			percent_team_two = f"{int(score_2 / percent_1)}%"
		except ZeroDivisionError:
			percent_team_one = "50%"
			percent_team_two = "50%"
		return percent_team_one, percent_team_two

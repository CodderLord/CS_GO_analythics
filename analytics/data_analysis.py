from parsing.help_file import first_same_name_dict, second_same_name_dict


class DataAnalysis:
	def __init__(self, name1, name2, history_score_dict, best_of_number, coefficient_dict, dict_old_scores, win_1, win_2):
		self.name_1: str = name1
		self.name_2: str = name2
		self.history_score_dict: dict or None = history_score_dict  # dict history scores if there is a history
		self.best_of_number: int = best_of_number  # number of best (bo1, bo2, bo3, bo5)
		self.coefficient_dict: dict = coefficient_dict  # coefficient on bookmakers
		self.dict_old_scores: dict = dict_old_scores  # dict which have team names(self.name_1, self.name_2) and their scores
		self.win_1: int = int(str(win_1).replace('-', '0'))  # score of winning team
		self.win_2: int = int(str(win_2).replace('-', '0'))
		self.first_same_teams: dict = first_same_name_dict  # dict which have names and scores same teams
		self.second_same_teams: dict = second_same_name_dict
		# -------------------------------------------
		self.percent_history_one, self.percent_history_two = self.calculate_history_score()
		self.percent_coefficient_one, self.percent_coefficient_two = self.calculate_coefficient()
		self.percent_form_one, self.percent_form_two = self.calculate_old_scores()
		self.percent_winning_one, self.percent_winning_two = self.calculate_winning()
		self.percent_same_one, self.percent_same_two = self.calculate_same_teams()

	def ret_all_value(self):
		return self.percent_history_one, self.percent_history_two, self.percent_coefficient_one, self.percent_coefficient_two, self.percent_form_one, self.percent_form_two, self.percent_winning_one, self.percent_winning_two, self.percent_same_one, self.percent_same_two

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
		print('history_score_dict')
		print(self.history_score_dict)
		print('percent_history_1, percent_history_2')
		print(percent_team_one, percent_team_two)
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
		print('coefficient_dict')
		print(self.coefficient_dict)
		print('percent_coefficient_1, percent_coefficient_2')
		print(percent_team_one, percent_team_two)
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
		print('old_scores')
		print(self.dict_old_scores)
		print('old_score_1, old_score_2')
		print(percent_team_one, percent_team_two)
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
		print('win1,win2')
		print(self.win_1, self.win_2)
		print('win_1, win_2')
		print(percent_team_one, percent_team_two)
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
		print('same_teams')
		print(self.first_same_teams)
		print(self.second_same_teams)
		print(first_same_score)
		print(second_same_score)
		print('percent_team_one, percent_team_two')
		print(percent_team_one, percent_team_two)
		return percent_team_one, percent_team_two

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

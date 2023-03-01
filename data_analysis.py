from help_file import first_same_name_dict, second_same_name_dict


class DataAnalysis:
	def __init__(self, name1, name2, history_score_dict, best_of_number, coefficient_dict, dict_old_scores, win_1, win_2):
		self.name_1: str = name1
		self.name_2: str = name2
		self.history_score_dict: dict or None = history_score_dict  # dict history scores if there is a history
		self.best_of_number: int = best_of_number  # number of best (bo1, bo2, bo3, bo5)
		self.coefficient_dict: dict = coefficient_dict  # coefficient on bookmakers
		self.dict_old_scores: dict = dict_old_scores
		self.win_1: int = int(str(win_1).replace('-', '0'))
		self.win_2: int = int(str(win_2).replace('-', '0'))
		self.first_same_teams: dict = first_same_name_dict
		self.second_same_teams: dict = second_same_name_dict
		self.scores_to_win_team_1 = 100
		self.scores_to_win_team_1 = 100
		# -------------------------------------------
		self.calculate_history_score()
		self.calculate_best_of_number()
		self.calculate_coefficient()
		self.calculate_old_scores()
		self.calculate_winning()
		self.calculate_same_teams()

	def calculate_history_score(self):
		print('history_score_dict')
		print(self.history_score_dict)
		try:
			score_1 = self.history_score_dict[self.name_1]
			score_2 = self.history_score_dict[self.name_2]
			percent_team_one, percent_team_two = self.calculate_percents(score_1, score_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		print('percent_history_1, percent_history_2')
		print(percent_team_one, percent_team_two)

	def calculate_best_of_number(self):
		print('best_of_number')
		print(self.best_of_number)

	def calculate_coefficient(self):
		print('coefficient_dict')
		print(self.coefficient_dict)
		try:
			coefficient_1 = self.coefficient_dict[self.name_1]
			coefficient_2 = self.coefficient_dict[self.name_2]
			percent_team_two, percent_team_one = self.calculate_percents(coefficient_1, coefficient_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		print('percent_coefficient_1, percent_coefficient_2')
		print(percent_team_one, percent_team_two)

	def calculate_old_scores(self):
		print('old_scores')
		print(self.dict_old_scores)
		try:
			old_score_1 = self.dict_old_scores[self.name_1]
			old_score_2 = self.dict_old_scores[self.name_2]
			percent_team_one, percent_team_two = self.calculate_percents(old_score_1, old_score_2)
		except TypeError:
			percent_team_one = '50%'
			percent_team_two = '50%'
		print('old_score_1, old_score_2')
		print(percent_team_one, percent_team_two)

	def calculate_winning(self):
		print('win1,win2')
		print(self.win_1, self.win_2)
		if self.win_1 != 0 and self.win_2 != 0:
			percent_team_one, percent_team_two = self.calculate_percents(self.win_1, self.win_2)
		else:
			percent_team_one = '50%'
			percent_team_two = '50%'
		print('win_1, win_2')
		print(percent_team_one, percent_team_two)

	def calculate_same_teams(self):
		print('same_teams')
		print(self.first_same_teams)
		print(self.second_same_teams)
		first_same_score = 0
		second_same_score = 0
		list_names_first = self.first_same_teams.keys()
		for i in list_names_first:
			first_same_score += int(first_same_name_dict[i].split('-')[0])
			second_same_score += int(first_same_name_dict[i].split('-')[1])
			# ------------------------------------------------------------
			second_same_score += int(first_same_name_dict[i].split('-')[0])
			first_same_score += int(first_same_name_dict[i].split('-')[1])
		print(first_same_score)
		print(second_same_score)
		if first_same_score != 0 and second_same_score != 0:
			percent_team_one, percent_team_two = self.calculate_percents(first_same_score, second_same_score)
		else:
			percent_team_one = '50%'
			percent_team_two = '50%'
		print('percent_team_one, percent_team_two')
		print(percent_team_one, percent_team_two)

	@staticmethod
	def calculate_percents(score_1, score_2):
		percent_100 = int(score_1) + int(score_2)
		percent_1 = percent_100 / 100
		percent_team_one = f"{int(score_1 / percent_1)}%"
		percent_team_two = f"{int(score_2 / percent_1)}%"
		return percent_team_one, percent_team_two

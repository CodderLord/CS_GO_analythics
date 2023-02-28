from help_file import first_same_name_dict, second_same_name_dict


class DataAnalysis:
	def __init__(self, history_score_dict, best_of_number, coefficient_dict, dict_old_scores, win_1, win_2):
		self.history_score_dict: dict or None = history_score_dict  # dict history scores if there is a history
		self.best_of_number: int = best_of_number  # number of best (bo1, bo2, bo3, bo5)
		self.coefficient_dict: dict = coefficient_dict  # coefficient on bookmakers
		self.dict_old_scores: dict = dict_old_scores
		self.win_1: int = win_1
		self.win_2: int = win_2
		self.first_same_teams: dict = first_same_name_dict
		self.second_same_teams: dict = second_same_name_dict
		# -------------------------------------------
		self.calculate_score()
		self.calculate_best_of_number()
		self.calculate_coefficient()
		self.calculate_old_scores()
		self.calculate_winning()
		self.calculate_same_teams()

	def calculate_score(self):
		print('history_score_dict')
		print(self.history_score_dict)

	def calculate_best_of_number(self):
		print('best_of_number')
		print(self.best_of_number)

	def calculate_coefficient(self):
		print('coefficient_dict')
		print(self.coefficient_dict)

	def calculate_old_scores(self):
		print('old_scores')
		print(self.dict_old_scores)

	def calculate_winning(self):
		print('win1,win2')
		print(self.win_1, self.win_2)

	def calculate_same_teams(self):
		print('same_teams')
		print(self.first_same_teams)
		print(self.second_same_teams)

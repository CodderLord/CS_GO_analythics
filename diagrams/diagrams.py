import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('QtAgg')
FIG, AX = plt.subplots()


def create_ratio_diagram(name1: str, name2: str, title: str, percent1: str, percent2: str, name: str):
	path_name = name1 + '_vs_' + name2
	teams = [name1, name2]
	counts = [int(percent1.replace('%', '')), int(percent2.replace('%', ''))]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	AX.bar(teams, counts, label=bar_labels, color=bar_colors)
	AX.set_facecolor('#132034')
	AX.set_ylabel('Соотношение(%)')
	AX.set_title(title)
	AX.legend(title='Цвет команд')
	plt.savefig(f'team_info/{path_name}/{name}.png')


def create_ratio_history_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Отношение истории игр команд')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_trend_history_diagram():
	# split the data into two parts
	xdata1 = [1, 5, 7, 8, 9, 14, 15, 17, 17, 19]
	col_games = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
	# plot the data
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	ax.plot(xdata1, color='tab:blue')
	ax.plot(col_games, color='tab:orange')
	ax.set_facecolor('xkcd:salmon')
	ax.set_facecolor('#132034')
	ax.set_title('Тенденция истории игр команд')
	ax.set_ylabel('Победы')
	ax.set_xlabel('Количество игр')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_coefficient_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Соотношения коефициентов команд')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_experience_teams_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Соотношение побед команд')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_form_team_diagram():
	# for team one and team two
	col_games = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1,  0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.21, 0.22]
	exodus_games = [111, 110, 104, 100, 80, 90, 88, 80, 77, 70, 66, 60, 55, 50, 44, 40, 33, 30, 22, 20, 11, 1] # 22
	fig, ax = plt.subplots()
	ax.plot(col_games, exodus_games)
	ax.set_xlim(0, col_games[-1])  # decreasing time
	ax.set_xlabel('Количество игр')
	ax.set_facecolor('#132034')
	ax.set_ylabel('Количество побед')
	ax.set_title('Команда name_team\n Тенденция побед команд по количеству игр. ')
	ax.grid(True)
	plt.show()
	# plt.savefig('saved_figure.png')


def create_ratio_form_team_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Отношение форм команд')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_ratio_same_teams_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']  # team_1 --> base team. team_2 --> same team
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Отношение побед команд')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


def create_result_teams_diagram():
	fig, ax = plt.subplots()
	teams = ['name_team_1', 'name_team_2']  # team_1 --> base team. team_2 --> same team
	counts = [20, 80]
	bar_labels = ['red', 'blue']
	bar_colors = ['tab:red', 'tab:blue']
	ax.bar(teams, counts, label=bar_labels, color=bar_colors)
	ax.set_facecolor('#132034')
	ax.set_ylabel('Соотношение(%)')
	ax.set_title('Общий результат')
	ax.legend(title='Цвет команд')
	plt.show()
	# plt.savefig('saved_figure.png')


#create_ratio_history_diagram()  # ratio
#create_trend_history_diagram()
#create_coefficient_diagram()  # ratio
#create_experience_teams_diagram()  # ratio
#create_form_team_diagram()
#create_ratio_form_team_diagram()  # ratio
#create_ratio_same_teams_diagram()  # ratio
#create_result_teams_diagram()  # ratio

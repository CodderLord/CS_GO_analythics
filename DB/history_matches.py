import sqlite3
from parsing.work_in_site import Connect


class DataBase:
	def __init__(self):
		self.__con = sqlite3.connect("DB/history_matches.db")  # for commit
		self.__cursor = self.__con.cursor()  # for execute --> fetchone/fetchall
		
	def check_match(self):
		self.__cursor.execute(f'''SELECT * FROM history_matches WHERE real_result IS NULL;''')
		rows = self.__cursor.fetchall()
		for id_match, title, bo, result, real_result, time_zone, url in rows:
			connect = Connect(url)
			score_1, score_2 = connect.find_score_post(url).split(" : ")
			score_1, score_2 = int(score_1), int(score_2)
			if score_1+score_2 != 0:
				if score_1 > score_2:
					name_result = title.split(' vs ')[0]
				elif score_1 < score_2:
					name_result = title.split(' vs ')[1]
				else:
					name_result = 'Ничья'
				self.__cursor.execute(f"UPDATE history_matches SET real_result = '{name_result}' WHERE id_matches = {id_match}")
				self.__con.commit()
		self.__cursor.close()
	
	def show_all_matches(self):
		self.__cursor.execute(f'''SELECT * FROM history_matches WHERE real_result IS NOT NULL;''')
		list_info = self.__cursor.fetchall()
		return list_info
	
	def commit_match(self, title_matches, bo_matches, program_result, time_analytic, link):
		_link = (link.replace('//', '/')).replace('/', '//', 1)
		self.__cursor.execute(f'''INSERT INTO history_matches (title_matches,bo_matches,program_result,time_analytic,link)
			VALUES ("{str(title_matches)}", {int(bo_matches)}, "{str(program_result)}", "{str(time_analytic)}", "{str(_link)}");''')
		self.__con.commit()
		self.__con.close()

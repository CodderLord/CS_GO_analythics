import sqlite3
from parsing.work_in_site import Connect


class DataBase:
	def __init__(self):
		self.con = sqlite3.connect("DB/history_matches.db")  # for commit
		self.cursor = self.con.cursor()  # for execute --> fetchone/fetchall
		
	def check_match(self):
		self.cursor.execute(f'''SELECT * FROM history_matches WHERE real_result is NULL;''')
		rows = self.cursor.fetchall()
		for id_match, title, bo, result, real_result, time_zone, url in rows:
			connect = Connect(url)
			score_1, score_2 = connect.find_score_post(url).split(" : ")
			if score_1 > score_2:
				result = 1
			if score_1 < score_2:
				result = -1
			if score_1 == score_2:
				result = 0
			self.cursor.execute(f"UPDATE history_matches SET real_result = {result} WHERE id_matches = {id_match}")
			self.con.commit()
		self.cursor.close()
	
	def show_all_matches(self):
		pass
	
	def commit_match(self, title_matches, bo_matches, program_result, time_analytic, link):
		link = (link.replace('//', '/')).replace('/', '//', 1)
		self.cursor.execute(f'''INSERT INTO history_matches (title_matches,bo_matches,program_result,time_analytic,link)
			VALUES ("{str(title_matches)}", {int(bo_matches)}, {int(program_result)}, "{str(time_analytic)}", "{str(link)}");''')
		self.con.commit()
		self.con.close()

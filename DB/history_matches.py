import sqlite3


class DataBase:
	def __init__(self):
		self.con = sqlite3.connect("DB/history_matches.db")  # for commit
		self.cursor = self.con.cursor()  # for execute --> fetchone/fetchall
	
	def show_all_matches(self):
		pass
	
	def commit_match(self, title_matches, bo_matches, program_result, time_analytic):
		self.cursor.execute(f'''INSERT INTO history_matches (title_matches,bo_matches,program_result,time_analytic)
		VALUES ("{str(title_matches)}", {int(bo_matches)}, {int(program_result)}, "{str(time_analytic)}")''')
		self.con.commit()
		self.con.close()

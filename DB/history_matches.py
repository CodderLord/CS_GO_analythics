import sqlite3


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect("history_mathes.db")  # for commit
        self.cursor = self.con.cursor()   # for execute --> fetchone/fetchall

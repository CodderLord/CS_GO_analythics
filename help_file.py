import datetime as dt

NOW_time = dt.datetime.now()

first_name_dict = {}
second_name_dict = {}
first_same_name_dict = {}
second_same_name_dict = {}

def translate_to_datatime(year: int, month: int, day: int, hour: int = 0, minute: int = 0):
	return dt.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

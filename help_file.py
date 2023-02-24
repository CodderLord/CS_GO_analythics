import datetime as dt

NOW_time = dt.datetime.now()


def translate_to_datatime(year: int, month: int, day: int, hour: int = 0, minute: int = 0):
	return dt.datetime(year=year, month=month, day=day, hour=hour, minute=minute)

from datetime import datetime

def timestamp_to_data_time(timestamp):
	if not timestamp:
		raise ValueError("timestamp must not be empty")
	elif type(timestamp).__name__ != 'int':
		raise ValueError("timestamp must be integer")
	date_time_obj = datetime.fromtimestamp(timestamp)
	date_time = date_time_obj.strftime("%I:%M %p, %d %b %Y")
	return date_time
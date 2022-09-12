from datetime import datetime
import xml.etree.ElementTree as ET
import re

def timestamp_to_data_time(timestamp):
	if not timestamp:
		raise ValueError("timestamp must not be empty")
	elif type(timestamp).__name__ != 'int':
		raise TypeError("timestamp must be integer")
	date_time_obj = datetime.fromtimestamp(timestamp)
	date_time = date_time_obj.strftime("%I:%M %p, %d %b %Y")
	return date_time

def parse_xml(xml):
	if not xml:
		raise ValueError("input xml can't be empty")
	elif type(xml).__name__ != 'str':
		raise TypeError("input xml must be string")

	paste_list = []
	xml = '<Data>' + xml + '</Data>'
	root = ET.fromstring(xml)
	for paste in root:
		paste_item = {}
		for item in paste:
			paste_item[item.tag] = item.text
		paste_list.append(paste_item)
	return paste_list

def sort_on(item):
	return item['paste_date']

def get_key_from_url(url,pattern):
	if not url or not pattern:
		raise ValueError("Url and pattern can't be empty")
	elif type(url).__name__ != 'str' or type(pattern).__name__ != 'str':
		raise ValueError("Url and pattern both should be string")
	
	m = re.search(pattern,url)
	if m:
		x = re.split(pattern,url,1)
		key = x[-1]
		if "/" in key:
			return (False,None)
		else:
			return (True,key)
	else:
		return (False,None)
	
	
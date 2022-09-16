import logging
from Quick_Paste.utility import *

class Logger:
	def __init__(self):
		try:
			self.env = "" 
			file_path = get_file_path("logs/quick_paste.log")
			logging.basicConfig(level=logging.ERROR,filename=file_path, filemode='a',datefmt="%I:%M %p, %d %b %Y ",format='%(asctime)s -> %(message)s')
		except PermissionError as e:
			self.consoleLog("Error: {}".format(e))
		except:
			self.consoleLog("Error: error is occuring while initializing logging module")


	def debug(self,msg):
		try:
			self.consoleLog("Debug: {}".format(msg))
			logging.debug("Debug: {}".format(msg))
		except:
			self.consoleLog("Debug: {}".format(msg))
		
		

	def error(self,msg):
		try:
			self.consoleLog("Error: {}".format(msg))
			logging.error("Error: {}".format(msg))
		except:
			self.consoleLog("Error: {}".format(msg))
		

	def info(self,msg):
		try:
			self.consoleLog("Info: {}".format(msg))
			logging.info("Info: {}".format(msg))
		except:
			self.consoleLog("Info: {}".format(msg))
		
	def consoleLog(self,msg):
		if self.env == 'dev':
			print(msg)


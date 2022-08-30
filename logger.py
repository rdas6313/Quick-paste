import logging

class Logger:
	def __init__(self,env="dev"):
		self.env = env

	def debug(self,msg):
		#logging.debug(msg)
		print("Debug: {}".format(msg))

	def error(self,msg):
		#logging.error(msg)
		print("Error: {}".format(msg))
		pass

	def info(self,msg):
		#logging.info(msg)
		print("Info: {}".format(msg))
		pass
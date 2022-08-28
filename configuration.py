from .logger import Logger
import json
import os

class Configuration:

	CLASS_NAME = "Configuration"
	FILE_NAME = 'config.json'

	def __init__(self):
		self.log = Logger()
		self.configs = {}
		self.loadConfig()


	def getConfigPath(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		config_path = os.path.join(dir_path,self.FILE_NAME)
		self.log.debug("{}: {}".format(self.CLASS_NAME,config_path))
		return config_path

	def loadConfig(self):
		try:
			with open(self.getConfigPath(), 'r') as config_file:
				config = json.load(config_file)
				for key in config.keys():
					self.configs[key] = config[key]

		except FileNotFoundError as e:
			self.log.error("{}: {}".format(self.CLASS_NAME,e))
		except:
			self.log.error("{}: Unknown Error".format(self.CLASS_NAME))

	def getConfig(self):
		return self.configs

		
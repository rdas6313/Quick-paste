from .logger import Logger
import json
import os
import copy


class ConfigType:
	API_KEY = "api_dev_key"
	PASTE_URL = "paste_url"
	BASE_URL = "base_url"
	GENERAL_ERROR_MSG = "general_error_msg"
	CLIENT_ERROR_MSG = "client_error_msg"
	SERVER_ERROR_MSG = "server_error_msg"
	REDIRECT_ERROR_MSG = "redirect_error_msg"
	INFO_ERROR_MSG = "info_error_msg"
	SUCCESS_PASTE_MSG = "success_paste_msg"
	USER_KEY = "api_user_key"
	LOGIN_URL = "user_login_url" 
	EMPTY_PASTE_NAME = "empty_paste_name_msg"
	CANCEL_PASTE = "cancel_pasting_msg"
	PASTE_NAME_INPUT_PLACEHOLDER = "paste_name_input_placholder_msg"
	PASTE_NAME_CAPTION = "paste_name_caption"
	SELECT_FROM_ITEMS = "select_from_items_msg"
	EMPTY_USER_NAME = "empty_user_name_msg"
	EMPTY_PASSWORD = "empty_password_msg"
	USER_NAME_CAPTION = "user_name_caption"
	USER_NAME_INPUT_PLACEHOLDER = "user_name_input_placeholder_msg"
	PASSWORD_INPUT_CAPTION = "password_input_caption"
	UNKNOWN_ERROR_MSG = "unknown_error_msg"
	USER_KEY_REMOVED_MSG = "user_key_removed_msg"
	USER_LIST_URL = PASTE_URL
	GET_USER_PASTE = "fetch_user_paste_url"
	RAISE_ISSUE_MSG = "raise_issue_msg"
	EMPTY_PASTE_LIST = "empty_paste_list_msg"
	NO_TITLE = "no_title_found"
	PUBLIC_RAW_PASTE_URL = "public_raw_paste_url"


class Configuration:

	__CLASS_NAME = "Configuration"
	__FILE_NAME = 'config.json'

	def __init__(self):
		self.log = Logger()
		self.__configs = {}
		self.__loadConfig()


	def __getConfigPath(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		config_path = os.path.join(dir_path,self.__FILE_NAME)
		self.log.debug("{}: {}".format(self.__CLASS_NAME,config_path))
		return config_path

	def __loadConfig(self):
		try:
			with open(self.__getConfigPath(), 'r') as config_file:
				config = json.load(config_file)
				for key in config.keys():
					self.__configs[key] = config[key]

		except FileNotFoundError as e:
			self.log.error("{}: {} while loading configuration".format(self.__CLASS_NAME,e))
		except:
			self.log.error("{}: Unknown Error while loading configuration".format(self.__CLASS_NAME))

	def getConfig(self):
		return copy.deepcopy(self.__configs)

	def updateConfig(self,key,value):
		if not self.__configs:
			return (False,"Configuration not loaded from file. First load the configuration then update")

		try:
			if type(key) is not str or type(value) is not str:
				raise ValueError("key and value must be string type")
			self.__configs[key] = value
			with open(self.__getConfigPath(),'w') as config_file:
				json.dump(self.__configs,config_file,indent=4,sort_keys=True)

		except FileNotFoundError as e:
			self.log.error("{}: {} where key {} and value {}".format(self.__CLASS_NAME,e,key,value))
		except ValueError as e:
			self.log.error("{}: {} where key {} and value {}".format(self.__CLASS_NAME,e,key,value))
		except:
			self.log.error("{}: Unknown Error where key {} and value {}".format(self.__CLASS_NAME,key,value))
		else:
			return (True,"Updated successfully")

		return (False,"Some error occured while updating.")






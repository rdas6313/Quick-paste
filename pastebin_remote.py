from .logger import Logger
from .http import *
#import http.client as http
from urllib.parse import quote
from .configuration import *
import json
import os


class PasteType:
	PUBLIC = "0"
	UNLISTED = "1"
	PRIVATE = "2"

class PasteExpire:
	NEVER = "N"
	YEAR = "1Y"
	HALF_YEAR = "6M"
	MONTH = "1M"
	HALF_MONTH = "2W"
	WEEK = "1W"
	DAY = "1D"
	HOUR = "1H"
	MINUTE = "10M"

class User:
	GUEST = 0
	USER = 1

class Pastebin:
	API_PASTE_CODE  = "api_paste_code"
	API_PASTE_PRIVATE = "api_paste_private"
	API_PASTE_NAME = "api_paste_name"
	API_PASTE_EXPIRE = "api_paste_expire_date"
	API_PASTE_FORMAT = "api_paste_format"
	API_USER_KEY = "api_user_key"
	API_OPTION = "api_option"
	API_USER_NAME = "api_user_name"
	API_USER_PASSWORD = "api_user_password"
	API_RESULT_LIMIT = "api_results_limit"
	API_PASTE_KEY = "api_paste_key"

class PastebinDriver():

	__CLASS_NAME = "PastebinDriver"

	def __init__(self):
		self.log = Logger()
		self.configs = {}
		self.loadConfig()
		self.http = HttpClient()
		
	def loadConfig(self):
		config = Configuration()
		self.configs = config.getConfig() 

	def generatePayload(self,data): #data : dict
		payload = ""
		try:
			dataList = list(data.keys())
			self.log.debug(data)
			self.log.debug(dataList)
			for key in dataList:
				self.log.debug(""+key+":"+data[key])
				if key is Pastebin.API_PASTE_NAME or key is Pastebin.API_PASTE_CODE or key is Pastebin.API_USER_NAME or key is Pastebin.API_USER_PASSWORD:
					payload += key + '=' + quote(data[key])
				else:
					payload += key + '=' + data[key]	
				if key != dataList[-1]:
					payload += '&'


			self.log.debug(payload)
		except:
			self.log.error("PastebinRemote: Unknown error in generatePayload")
		finally:
			return payload

	def __postToServer(self,data,path):

		payload = self.generatePayload(data)
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		base_url = self.configs.get(ConfigType.BASE_URL,ConfigType.BASE_URL)	

		self.log.info("{}: Before sending to pastebin, data {}".format(self.__CLASS_NAME,data))

		status,msg = self.http.post(base_url,path,payload,headers)
		
		res_msg = ""
		is_success = False
		
		if status >= 100 and status < 200:
			res_msg = self.configs[ConfigType.INFO_ERROR_MSG]
		elif status >= 300 and status < 400:
			res_msg = self.configs[ConfigType.REDIRECT_ERROR_MSG]
		elif status >= 400 and status < 500:
			res_msg = self.configs[ConfigType.CLIENT_ERROR_MSG]
		elif status >= 500 and status < 600:
			res_msg = self.configs[ConfigType.SERVER_ERROR_MSG]
		else:
			is_success = True
		if msg:
			res_msg += msg

		self.log.info("{}: success {}, status {}, msg {}".format(self.__CLASS_NAME,is_success,status,res_msg))

		return (is_success,res_msg)


	def guestPush(self,paste_code,callable,paste_name="default"): #paste_code : str , callable : method(tuple) , paste_name : str
		
		api_option = "paste"

		data = {
			Pastebin.API_OPTION : api_option,
			Pastebin.API_PASTE_CODE : paste_code,
			Pastebin.API_PASTE_NAME : paste_name,
			Pastebin.API_PASTE_PRIVATE : PasteType.PUBLIC,
			Pastebin.API_PASTE_EXPIRE : PasteExpire.NEVER,
			ConfigType.API_KEY : self.configs.get(ConfigType.API_KEY,ConfigType.API_KEY),

		}
	
		#add paste format,get format and add it like data[Pastebin.API_PASTE_FORMAT] = ".c"

		path = self.configs.get(ConfigType.PASTE_URL,ConfigType.PASTE_URL)	

		is_success,res_msg = self.__postToServer(data,path)
		callable((is_success,res_msg))



	def getUserToken(self,username,password):
		
		if not username or not password:
			return (False,"Username and password can't be empty")
		elif type(username) is not str or type(password) is not str:
			return (False,"Username and password must be string")

		data = {
			ConfigType.API_KEY : self.configs.get(ConfigType.API_KEY,ConfigType.API_KEY),
			Pastebin.API_USER_NAME : username,
			Pastebin.API_USER_PASSWORD : password
		}

		path = self.configs.get(ConfigType.LOGIN_URL,ConfigType.LOGIN_URL)

		return self.__postToServer(data,path)



	def userPush(self,callable,token,code,name,expire=PasteExpire.NEVER,visibility=PasteType.PRIVATE,extension=""):
		if not token or not code or not name or not expire or not visibility:
			callable((False,"User token, Paste code, Paste name, Paste expire, Paste visibility can't be empty")) 
			return
		elif type(token) is not str or type(code) is not str or type(name) is not str or type(expire) is not str or type(visibility) is not str or type(extension) is not str:
			callable((False,"User token, Paste code, Paste name, Paste expire, Paste visibility, Paste format must be string"))
			return
			
		data = {
			Pastebin.API_OPTION : "paste",
			Pastebin.API_PASTE_CODE : code,
			Pastebin.API_PASTE_NAME : name,
			Pastebin.API_PASTE_PRIVATE : visibility,
			Pastebin.API_PASTE_EXPIRE : expire,
			Pastebin.API_USER_KEY : token,
			ConfigType.API_KEY : self.configs.get(ConfigType.API_KEY,ConfigType.API_KEY),
			Pastebin.API_PASTE_FORMAT : extension
		}

		path = self.configs.get(ConfigType.PASTE_URL,ConfigType.PASTE_URL)	

		is_success,res_msg = self.__postToServer(data,path)
		callable((is_success,res_msg))


	def getUserPasteList(self,callable,token,limit="1000"):
		
		if not callable or (type(callable).__name__ != 'method' and type(callable).__name__ != 'function'): 
			raise ValueError("callable must be a method or function and should not be empty")
		elif not token:
			raise ValueError("User token can't be empty")
		elif type(limit).__name__ != 'str' or type(token).__name__ != 'str':
			raise ValueError("User token and limit must be string")

		data = {
			Pastebin.API_OPTION : "list",
			Pastebin.API_RESULT_LIMIT : limit,
			Pastebin.API_USER_KEY : token,
			ConfigType.API_KEY : self.configs.get(ConfigType.API_KEY,ConfigType.API_KEY)
		}

		path = self.configs.get(ConfigType.USER_LIST_URL,ConfigType.USER_LIST_URL)
		is_success,res_msg = self.__postToServer(data,path)
		callable((is_success,res_msg))

	def getUserPaste(self,callable,token,paste_key):
		
		if not callable or (type(callable).__name__ != 'method' and type(callable).__name__ != 'function'): 
			raise ValueError("callable must be a method or function and should not be empty")
		elif not token or not paste_key:
			raise ValueError("User token, paste key or callable method can't be empty") 
		elif type(paste_key).__name__ != 'str' or type(token).__name__ != 'str':
			raise ValueError("User token and paste key must be string")
		
		data = {
			Pastebin.API_OPTION : "show_paste",
			Pastebin.API_USER_KEY : token,
			Pastebin.API_PASTE_KEY : paste_key,
			ConfigType.API_KEY : self.configs.get(ConfigType.API_KEY,ConfigType.API_KEY)
		}

		path = self.configs.get(ConfigType.GET_USER_PASTE,ConfigType.GET_USER_PASTE)
		is_success,msg = self.__postToServer(data,path)
		callable((is_success,msg))



		
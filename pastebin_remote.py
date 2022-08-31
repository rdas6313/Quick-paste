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
				if key is Pastebin.API_PASTE_NAME or key is Pastebin.API_PASTE_CODE:
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

		payload = self.generatePayload(data)
	
		#add paste format,get format and add it like data[Pastebin.API_PASTE_FORMAT] = ".c"
		
		headers = {
			'Content-Type': 'application/x-www-form-urlencoded'
		}

		base_url = self.configs.get(ConfigType.BASE_URL,ConfigType.BASE_URL)
		path = self.configs.get(ConfigType.PASTE_URL,ConfigType.PASTE_URL)	

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
		callable((is_success,res_msg))


		
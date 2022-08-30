from .logger import Logger
import http.client as http
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

class PastebinRemote:


	def __init__(self):
		self.log = Logger()
		self.configs = {}
		self.loadConfig()
		

	def getConfigPath(self):
		dir_path = os.path.dirname(os.path.realpath(__file__))
		config_path = os.path.join(dir_path,'config.json')
		return config_path
		

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

	def push(self,data): #data : dict
		conn = None
		res = None
		try:
			
			api_option = "paste"
			self.log.info("PastebinRemote Connecting to Pastebin server.")
			conn = http.HTTPSConnection(self.configs[ConfigType.BASE_URL])
			data[ConfigType.API_KEY] = self.configs[ConfigType.API_KEY]
			data[Pastebin.API_OPTION] = api_option
			payload = self.generatePayload(data)
			self.log.debug(payload)
			headers = {
			  'Content-Type': 'application/x-www-form-urlencoded'
			}			
			conn.request("POST", self.configs[ConfigType.PASTE_URL], payload, headers)
			res = conn.getresponse()
			res_data = res.read()
			data = res_data.decode("utf-8")
			self.log.info("PastebinRemote Response Code : {}".format(res.status))
			self.log.info("PastebinRemote Response Data : {}".format(data))
			

		except ValueError as e:
			self.log.error("PastebinRemote: {}".format(e))
		except InvalidURL as e:
			self.log.error("PastebinRemote: {}".format(e))
		except NotConnected as e:
			self.log.error("PastebinRemote: {}".format(e))
		except CannotSendRequest as e:
			self.log.error("PastebinRemote: {}".format(e))
		except HTTPException as e:
			self.log.error("PastebinRemote: {}".format(e))
		except:
			self.log.error("PastebinRemote: Unknown exception")
		finally:
			if conn:
				conn.close()
				self.log.info("PastebinRemote Connection is closed with server")
			else:
				self.log.error("PastebinRemote: Connection is null")
			if res:
				return (res.status,data)
			else:
				return (400,None)





class PastebinDriver(PastebinRemote):

	__CLASS_NAME = "PastebinDriver"

	def __init__(self):
		PastebinRemote.__init__(self)

	def guestPush(self,paste_code,callable,paste_name="default"): #paste_code : str , callable : method(tuple) , paste_name : str
		data = {
			Pastebin.API_PASTE_CODE : paste_code,
			Pastebin.API_PASTE_NAME : paste_name,
			Pastebin.API_PASTE_PRIVATE : PasteType.PUBLIC,
			Pastebin.API_PASTE_EXPIRE : PasteExpire.NEVER
		}
	
		#add paste format,get format and add it like data[Pastebin.API_PASTE_FORMAT] = ".c"
		
		self.log.info("{}: Before sending to pastebin, data {}".format(self.__CLASS_NAME,data))
		status,msg = self.push(data)
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


		
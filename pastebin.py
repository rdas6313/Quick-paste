from .sublime_api import SublimeApi
from .pastebin_remote import *
from .configuration import *

class Paste:

	PASTE_EXPIRE = {
		"NEVER" : "N",
		"1 YEAR" : "1Y",
		"HALF_YEAR" : "6M",
		"MONTH" : "1M",
		"HALF_MONTH" : "2W",
		"WEEK" : "1W",
		"DAY" : "1D",
		"HOUR" : "1H",
		"MINUTE" : "10M"
	}

	PASTE_VISIBILITY = {
		"PUBLIC" : "0",
		"PRIVATE" : "2",
		"UNLISTED" : "1"
	}

	def init(self):
		self.configs = {}
		self.remote = PastebinDriver()
		self.loadConfig()

	def loadConfig(self):
		self.config_obj = Configuration()
		self.configs = self.config_obj.getConfig()

	def onDone(self,data):
		is_success,msg = data
		if(is_success):
			success_msg = msg + self.configs.get(ConfigType.SUCCESS_PASTE_MSG,None)
			self.copy(msg)
			self.showMessage(success_msg)
		else:
			self.showErrorMessage(msg)



class GuestPaste(SublimeApi):
	def init(self):
		self.configs = {}
		self.remote = PastebinDriver()
		self.loadConfig()

	def loadConfig(self):
		config = Configuration()
		self.configs = config.getConfig()
		
	def sendContent(self):
		paste_code = self.getContent()
		paste_name = self.getFileName()
		self.remote.guestPush(paste_code,self.onDone,paste_name)

	def onDone(self,data):
		is_success,msg = data
		if(is_success):
			success_msg = msg + self.configs.get(ConfigType.SUCCESS_PASTE_MSG,None)
			self.copy(msg)
			self.showMessage(success_msg)
		else:
			self.showErrorMessage(msg)

	def run(self,edit):
		try:
			self.init()	
			self.runInBackground(self.sendContent)
		except ImportError as e:
			self.log.error("GuestPaste: {}".format(e))
		except FileNotFoundError as e:
			self.log.error("GuestPaste: {}".format(e))
		except RuntimeError as e:
			self.log.error("GuestPaste: {}".format(e))
		except:
			self.log.error("GuestPaste: Unknown Error")


class UserPaste(Paste,SublimeApi):

	__CLASS_NAME = "UserPaste"

	def on_paste_name(self,data):
		if not data:
			self.showMessage("Paste name is empty. So Default name '{}' will be used.".format(self.data["name"]))
		self.data["name"] = data
		self.selectFromList(self.expire,self.on_select_expire,"Select from list")
		

	def on_select_expire(self,index):
		if index < 0:
			self.showMessage("Hummm! So you choose not to paste now.")
			return
		key = self.expire[index]
		value = self.PASTE_EXPIRE[key]
		self.data["expire"] = value
		self.selectFromList(self.vis,self.on_select_visibility,"Select from list")

	def on_select_visibility(self,index):
		if index < 0:
			self.showMessage("Hummm! So you choose not to paste now.")
			return
		key = self.vis[index]
		value = self.PASTE_VISIBILITY[key]
		self.data["vis"] = value
		self.sendContent()

	def sendContent(self):
		self.remote.userPush(
			self.onDone,
			self.data["user_key"],
			self.data["code"],
			self.data["name"],
			self.data["expire"],
			self.data["vis"]
		)


	def on_user_name(self,name):
		if not name:
			self.showErrorMessage("User name field can't be empty")
			return
		self.data["user_name"] = name 
		self.inputPassword("Password",self.on_password)
		

	def on_password(self,password):
		if not password:
			self.showErrorMessage("Password field can't be empty")
			return
		self.data["password"] = password
		is_success,msg = self.remote.getUserToken(self.data["user_name"],self.data["password"])
		if is_success:
			self.data["user_key"] = msg
			self.config_obj.updateConfig(ConfigType.USER_KEY,msg)
			self.prepareToSend()
		else:
			self.showErrorMessage(msg)

	def prepareToSend(self):
		self.data["code"] = self.getContent()
		self.data["name"] = self.getFileName()
		self.expire = list(self.PASTE_EXPIRE.keys())
		self.vis = list(self.PASTE_VISIBILITY.keys())
		self.inputText("Paste name",self.data.get("name","Enter paste name"),self.on_paste_name)

	def startProcessing(self):
		user_key = self.configs.get(ConfigType.USER_KEY,None)
		self.data = {}
		if not user_key:
			self.inputText("User name","Enter pastebin user name",self.on_user_name)
			return

		self.data["user_key"] = user_key
		self.prepareToSend()

	def run(self,edit):
		try:
			
			self.init()
			self.runInBackground(self.startProcessing)

		except ImportError as e:
			self.log.error("{}: {}".format(self.__CLASS_NAME,e))
		except FileNotFoundError as e:
			self.log.error("{}: {}".format(self.__CLASS_NAME,e))
		except RuntimeError as e:
			self.log.error("{}: {}".format(self.__CLASS_NAME,e))
		except:
			self.log.error("{}: Unknown Error".format(self.__CLASS_NAME))


	

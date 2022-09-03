from .sublime_api_helper import SublimeApiHelper
from .pastebin_remote import *
from .configuration import *
from .logger import Logger
import sublime_plugin

class CommonPasteCommand(sublime_plugin.TextCommand):

	PASTE_EXPIRE = {
		"Expire never" : PasteExpire.NEVER,
		"Expire in 1 year" : PasteExpire.YEAR,
		"Expire in 6 months" : PasteExpire.HALF_YEAR,
		"Expire in 1 month" : PasteExpire.MONTH,
		"Expire in 15 days" : PasteExpire.HALF_MONTH,
		"Expire in 1 weeks" : PasteExpire.WEEK,
		"Expire in 1 day" : PasteExpire.DAY,
		"Expire in 1 hour" : PasteExpire.HOUR,
		"Expire in 1 minute" : PasteExpire.MINUTE
	}

	PASTE_VISIBILITY = {
		"Public paste" : PasteType.PUBLIC,
		"Private paste" : PasteType.PRIVATE,
		"Unlisted paste" : PasteType.UNLISTED
	}

	def __init(self):
		self.log = Logger()
		self.helper = SublimeApiHelper(self)
		self.configs = {}
		self.remote = PastebinDriver()
		self.__loadConfig()

	def __loadConfig(self):
		self.config_obj = Configuration()
		self.configs = self.config_obj.getConfig()

	def on_paste_done(self,data):
		is_success,msg = data
		if(is_success):
			success_msg = msg + self.configs.get(ConfigType.SUCCESS_PASTE_MSG,None)
			self.helper.copy(msg)
			self.helper.showMessage(success_msg)
		else:
			self.helper.showErrorMessage(msg)


	def on_start_command(self):
		pass

	def run(self,edit):
		try:
			
			self.__init()	
			self.helper.runInBackground(self.on_start_command)

		except ImportError as e:
			self.log.error("{}: {}".format(type(self).__name__,e))
		except FileNotFoundError as e:
			self.log.error("{}: {}".format(type(self).__name__,e))
		except RuntimeError as e:
			self.log.error("{}: {}".format(type(self).__name__,e))
		except:
			self.log.error("{}: Unknown Error".format(type(self).__name__))



class GuestPasteCommand(CommonPasteCommand):
		
	def on_start_command(self):
		paste_code = self.helper.getContent()
		paste_name = self.helper.getFileName()
		self.remote.guestPush(paste_code,self.on_paste_done,paste_name)

class UserPasteCommand(CommonPasteCommand):

	__CLASS_NAME = "UserPaste"

	def on_paste_name(self,data):
		if not data:
			self.helper.showMessage("Paste name is empty. So Default name '{}' will be used.".format(self.data["name"]))
		self.data["name"] = data
		self.helper.selectFromList(self.expire,self.on_select_expire,"Select from list")
		

	def on_select_expire(self,index):
		if index < 0:
			self.helper.showMessage("Hummm! So you choose not to paste now.")
			return
		key = self.expire[index]
		value = self.PASTE_EXPIRE[key]
		self.data["expire"] = value
		self.helper.selectFromList(self.vis,self.on_select_visibility,"Select from list")

	def on_select_visibility(self,index):
		if index < 0:
			self.helper.showMessage("Hummm! So you choose not to paste now.")
			return
		key = self.vis[index]
		value = self.PASTE_VISIBILITY[key]
		self.data["vis"] = value
		self.sendContent()

	def sendContent(self):
		self.remote.userPush(
			self.on_paste_done,
			self.data["user_key"],
			self.data["code"],
			self.data["name"],
			self.data["expire"],
			self.data["vis"]
		)


	def on_user_name(self,name):
		if not name:
			self.helper.showErrorMessage("User name field can't be empty")
			return
		self.data["user_name"] = name 
		self.helper.inputPassword("Password",self.on_password)
		

	def on_password(self,password):
		if not password:
			self.helper.showErrorMessage("Password field can't be empty")
			return
		self.data["password"] = password
		is_success,msg = self.remote.getUserToken(self.data["user_name"],self.data["password"])
		if is_success:
			self.data["user_key"] = msg
			self.config_obj.updateConfig(ConfigType.USER_KEY,msg)
			self.prepareToSend()
		else:
			self.helper.showErrorMessage(msg)

	def prepareToSend(self):
		self.data["code"] = self.helper.getContent()
		self.data["name"] = self.helper.getFileName()
		self.expire = list(self.PASTE_EXPIRE.keys())
		self.vis = list(self.PASTE_VISIBILITY.keys())
		self.helper.inputText("Paste name",self.data.get("name","Enter paste name"),self.on_paste_name)

	def on_start_command(self):
		user_key = self.configs.get(ConfigType.USER_KEY,None)
		self.data = {}
		if not user_key:
			self.helper.inputText("User name","Enter pastebin user name",self.on_user_name)
			return

		self.data["user_key"] = user_key
		self.prepareToSend()


	

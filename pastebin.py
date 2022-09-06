from .sublime_api_helper import SublimeApiHelper
from .pastebin_remote import *
from .configuration import *
from .logger import Logger
import sublime_plugin

class PasteTool(sublime_plugin.TextCommand):

	def __init(self):
		self.log = Logger()
		self.helper = SublimeApiHelper(self)
		self.configs = {}
		self.remote = PastebinDriver()
		self.__loadConfig()

	def __loadConfig(self):
		self.config_obj = Configuration()
		self.configs = self.config_obj.getConfig()

	def on_user_name(self,name):
		if not name:
			self.helper.showErrorMessage(self.configs.get(ConfigType.EMPTY_USER_NAME,None))
			return
		self.data["user_name"] = name 
		self.generateUserToken()
		
	def on_password(self,password):
		if not password:
			self.helper.showErrorMessage(self.configs.get(ConfigType.EMPTY_PASSWORD,None))
			return
		self.data["password"] = password
		self.generateUserToken()

	def on_user_token(self,is_generated):
		pass

	def generateUserToken(self):
		if not self.data.get("user_name",None):
			self.helper.inputText(self.configs.get(ConfigType.USER_NAME_CAPTION,None),self.configs.get(ConfigType.USER_NAME_INPUT_PLACEHOLDER,None),self.on_user_name)
			return
		elif not self.data.get("password",None):
			self.helper.inputPassword(self.configs.get(ConfigType.PASSWORD_INPUT_CAPTION,None),self.on_password)
			return
		
		is_success,msg = self.remote.getUserToken(self.data["user_name"],self.data["password"])
		if is_success:
			self.data["user_key"] = msg
			self.config_obj.updateConfig(ConfigType.USER_KEY,msg)
			self.on_user_token(True)
		else:
			self.helper.showErrorMessage(msg)
			self.on_user_token(False)

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
			self.log.error("{}: {}".format(type(self).__name__),self.configs.get(ConfigType.UNKNOWN_ERROR_MSG,None))



class CommonPaste(PasteTool):

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

	
	def on_paste_done(self,data):
		is_success,msg = data
		if(is_success):
			success_msg = msg + self.configs.get(ConfigType.SUCCESS_PASTE_MSG,None)
			self.helper.copy(msg)
			self.helper.showMessage(success_msg)
		else:
			self.helper.showErrorMessage(msg)


class GuestPasteCommand(CommonPaste):
		
	def on_start_command(self):
		paste_code = self.helper.getContent()
		paste_name = self.helper.getFileName()
		self.remote.guestPush(paste_code,self.on_paste_done,paste_name)

class UserPasteCommand(CommonPaste):

	def on_paste_name(self,data):
		if not data:
			data = self.helper.getFileName()
			self.helper.showMessage(self.configs.get(ConfigType.EMPTY_PASTE_NAME,None).format(data))
			
		self.data["name"] = data
		self.collectUserPrefs()

	def on_select_expire(self,index):
		if index < 0:
			self.helper.showMessage(self.configs.get(ConfigType.CANCEL_PASTE,None))
			return
		key = self.expire[index]
		value = self.PASTE_EXPIRE[key]
		self.data["expire"] = value
		self.collectUserPrefs()

	def on_select_visibility(self,index):
		if index < 0:
			self.helper.showMessage(self.configs.get(ConfigType.CANCEL_PASTE))
			return
		key = self.vis[index]
		value = self.PASTE_VISIBILITY[key]
		self.data["vis"] = value
		self.collectUserPrefs()


	def on_collect_prefs(self):
		self.remote.userPush(
			self.on_paste_done,
			self.data["user_key"],
			self.data["code"],
			self.data["name"],
			self.data["expire"],
			self.data["vis"]
		)

	def prepareToSend(self):
		self.data["code"] = self.helper.getContent()
		file_name = self.helper.getFileName() if self.helper.getFileName() else self.configs.get(ConfigType.PASTE_NAME_INPUT_PLACEHOLDER,None)
		self.expire = list(self.PASTE_EXPIRE.keys())
		self.vis = list(self.PASTE_VISIBILITY.keys())
		self.collectUserPrefs(file_name)

	def collectUserPrefs(self,file_name=None):

		if not self.data.get("name",None):
			self.helper.inputText(self.configs.get(ConfigType.PASTE_NAME_CAPTION,None),file_name,self.on_paste_name)
			return
		elif not self.data.get("expire",None):
			self.helper.selectFromList(self.expire,self.on_select_expire,self.configs.get(ConfigType.SELECT_FROM_ITEMS,None))
			return
		elif not self.data.get("vis",None):
			self.helper.selectFromList(self.vis,self.on_select_visibility,self.configs.get(ConfigType.SELECT_FROM_ITEMS,None))
			return

		self.on_collect_prefs()
	

	def on_user_token(self,generated):
		if not generated:
			return
		self.prepareToSend()

	def on_paste_done(self,data):
		is_success,msg = data

		key = self.convert_response_msg_to_config_key(msg)
		if key == ConfigType.USER_KEY:
			self.config_obj.updateConfig(ConfigType.USER_KEY,"")
			msg += self.configs.get(ConfigType.USER_KEY_REMOVED_MSG,None)
		
		super().on_paste_done((is_success,msg))


	def convert_response_msg_to_config_key(self,msg):
		if not msg:
			return None
		msgs = msg.split(" ")
		return msgs[-1].strip()

	def on_start_command(self):
		user_key = self.configs.get(ConfigType.USER_KEY,None)
		self.data = {}
		if not user_key:
			self.generateUserToken()
			return

		self.data["user_key"] = user_key
		self.prepareToSend()


	

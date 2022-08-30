from .sublime_api import SublimeApi
from .pastebin_remote import *
from .configuration import *

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

	

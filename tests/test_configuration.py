from unittesting import DeferrableTestCase
from Quick_Paste.configuration import *

class TestConfiguration(DeferrableTestCase):

	def setUp(self):
		self.remote = Configuration()

	def test_getConfigPath(self):
		pass
		#path = "/home/rdas6313/.config/sublime-text/Packages/Quick_Paste/config.json"
		#self.assertEqual(self.remote.getConfigPath(),path)

	def test_loadConfig(self):
		pass
		#self.remote.loadConfig()
		#configs = self.remote.configs
		#key = configs[ConfigType.API_KEY]
		#paste_url = configs[ConfigType.PASTE_URL]
		#base_url = configs[ConfigType.BASE_URL]
		#general_error_msg = configs[ConfigType.GENERAL_ERROR_MSG]
		#self.assertTrue(configs)
		#self.assertEqual(paste_url,"/api/api_post.php")
		#self.assertEqual(key,"AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3")
		#self.assertEqual(base_url,"pastebin.com")
		#self.assertEqual(general_error_msg,"Oops! Some unexpected error happened. \n")

	def test_getConfig(self):
		configs = self.remote.getConfig()
		key = configs[ConfigType.API_KEY]
		paste_url = configs[ConfigType.PASTE_URL]
		base_url = configs[ConfigType.BASE_URL]
		general_error_msg = configs[ConfigType.GENERAL_ERROR_MSG]
		self.assertTrue(configs)
		self.assertEqual(paste_url,"/api/api_post.php")
		self.assertEqual(key,"AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3")
		self.assertEqual(base_url,"pastebin.com")
		self.assertEqual(general_error_msg,"Oops! Some unexpected error happened. \n")

	def test_deepcopy(self):
		configs = self.remote.getConfig()
		configs[ConfigType.USER_KEY] = "raja"
		configs2 = self.remote.getConfig()
		#print("original : {}, change: {}".format(configs2[ConfigType.USER_KEY],configs[ConfigType.USER_KEY]))
		self.assertNotEqual(configs2[ConfigType.USER_KEY],configs[ConfigType.USER_KEY])
		


	def test_updateConfig(self):
		success,msg = self.remote.updateConfig(ConfigType.USER_KEY,"abcdef")
		self.assertTrue(success)

	def test_updateConfig_with_empty_key(self):
		success,msg = self.remote.updateConfig(None,"abcdef")
		self.assertFalse(success)

	def test_updateConfig_with_empty_value(self):
		success,msg = self.remote.updateConfig("api_user_key",None)
		self.assertFalse(success)

	def test_updateConfig_with_non_string_value(self):
		success,msg = self.remote.updateConfig("api_user_key",2)
		self.assertFalse(success)

	def test_updateConfig_with_non_string_key(self):
		success,msg = self.remote.updateConfig(2,"Abcdedf")
		self.assertFalse(success)

	
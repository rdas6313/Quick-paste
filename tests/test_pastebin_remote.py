from unittesting import DeferrableTestCase
from Quick_Paste.pastebin_remote import *


class TestPastebinRemote(DeferrableTestCase):

	def setUp(self):
		self.remote = PastebinRemote()

	def test_loadConfig(self):
		self.remote.loadConfig()
		configs = self.remote.configs
		key = configs[ConfigType.API_KEY]
		paste_url = configs[ConfigType.PASTE_URL]
		base_url = configs[ConfigType.BASE_URL]
		general_error_msg = configs[ConfigType.GENERAL_ERROR_MSG]
		self.assertTrue(configs)
		self.assertEqual(paste_url,"/api/api_post.php")
		self.assertEqual(key,"AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3")
		self.assertEqual(base_url,"pastebin.com")
		self.assertEqual(general_error_msg,"Oops! Some unexpected error happened. \n")
	
	def test_getConfigPath(self):
		path = self.remote.getConfigPath()
		actual_path = "/home/rdas6313/.config/sublime-text/Packages/Quick_Paste/config.json"
		self.assertEqual(path,actual_path)

	def test_generatePayload_correct_data(self):
		data = { "api_dev_key" : "AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3" ,"api_paste_code" : "Generate Paste example" }
		actual_payload = self.remote.generatePayload(data)
		payload = "api_dev_key=AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3&api_paste_code=Generate%20Paste%20example"
		#self.assertEqual(actual_payload,payload)

	def test_generatePayload_correct_data_2(self):
		data = {'api_paste_code': 'sample code', 'api_paste_private': "0", 'api_paste_expire_date': 'N', 'api_paste_name': 'sample paste name'}
		payload = self.remote.generatePayload(data)
		result_shoould_be = "api_paste_code=sample%20code&api_paste_private=0&api_paste_expire_date=N&api_paste_name=sample paste name"
		#self.assertEqual(payload,result_shoould_be)

	def test_generatePayload_no_data(self):
		self.assertRaises(Exception,self.remote.generatePayload(None))
		#pass

	def test_generatePayload_wrong_type_data(self):
		data = ["raja","das","abc"]
		self.assertRaises(Exception,self.remote.generatePayload(data))		
		#pass

	def test_push_with_correct_data(self):
		paste_data = { "api_paste_code" : "Paste Test code" }
		#res_code,msg = self.remote.push(paste_data)
		#self.assertEqual(res_code,200)

	def test_push_wrong_data(self):
		pass
		#paste_data = { "api_paste_codwest" : "paste_code" }
		#res_code,msg = self.remote.push(paste_data)
		#self.assertNotEqual(res_code,200)

	def test_push_no_data(self):
		pass
		#status,msg = self.remote.push(None)
		#self.assertEqual(status,400)
		#self.assertFalse(msg)


from unittesting import DeferrableTestCase
from Quick_Paste.pastebin_remote import *
import sublime

class TestPastebinDriver(DeferrableTestCase):
	
	def setUp(self):
		self.remote = PastebinDriver()

	def on_done(self,data):
		success,msg = data
		self.assertEqual(success,True)

	def test_guestPush(self):		
		#self.remote.guestPush("Sample code",self.on_done,"sample title")
		pass
	
	def test_guestPush_with_no_callable(self):
		#self.remote.guestPush("Sample code",None,"sample title")
		pass

	def test_guestPush_with_no_content(self):
		#self.remote.guestPush(None,self.on_done,"sample title")
		pass

	def test_guestPush_with_empty_content(self):
		#self.remote.guestPush("",self.on_done,"sample title")
		pass

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
	

	def test_generatePayload_correct_data(self):
		data = { "api_dev_key" : "AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3" ,"api_paste_code" : "Generate Paste example" }
		actual_payload = self.remote.generatePayload(data)
		payload = "api_dev_key=AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3&api_paste_code=Generate%20Paste%20example"
		self.assertEqual(actual_payload,payload)

	def test_generatePayload_correct_data_2(self):
		data = {'api_paste_code': 'sample code', 'api_paste_private': "0", 'api_paste_expire_date': 'N', 'api_paste_name': 'sample paste name'}
		payload = self.remote.generatePayload(data)
		result_shoould_be = "api_paste_code=sample%20code&api_paste_private=0&api_paste_expire_date=N&api_paste_name=sample%20paste%20name"
		self.assertEqual(payload,result_shoould_be)

	def test_generatePayload_no_data(self):
		self.assertRaises(Exception,self.remote.generatePayload(None))
		#pass

	def test_generatePayload_wrong_type_data(self):
		data = ["raja","das","abc"]
		self.assertRaises(Exception,self.remote.generatePayload(data))		
		#pass

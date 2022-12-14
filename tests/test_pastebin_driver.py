from unittesting import DeferrableTestCase
from Quick_Paste.pastebin_remote import *
import sublime

class TestPastebinDriver(DeferrableTestCase):
	
	def setUp(self):
		self.remote = PastebinDriver()

	def on_done(self,data):
		success,msg = data
		print(msg)
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
		#actual_payload = self.remote.generatePayload(data)
		#payload = "api_dev_key=AIKXQEl1Z3pZhZO1q7afM7LOrAkZ5uE3&api_paste_code=Generate%20Paste%20example"
		#self.assertEqual(actual_payload,payload)

	def test_generatePayload_correct_data_2(self):
		data = {'api_paste_code': 'sample code', 'api_paste_private': "0", 'api_paste_expire_date': 'N', 'api_paste_name': 'sample paste name'}
		#payload = self.remote.generatePayload(data)
		#result_shoould_be = "api_paste_code=sample%20code&api_paste_private=0&api_paste_expire_date=N&api_paste_name=sample%20paste%20name"
		#self.assertEqual(payload,result_shoould_be)

	def test_generatePayload_no_data(self):
		self.assertRaises(Exception,self.remote.generatePayload(None))
		#pass

	def test_generatePayload_wrong_type_data(self):
		data = ["raja","das","abc"]
		self.assertRaises(Exception,self.remote.generatePayload(data))		
		#pass

	def test_getUserToken(self):
		username = ""
		password = "s"
		#success,msg = self.remote.getUserToken(username,password)
		#self.assertTrue(success)

	def test_getUserToken_with_empty_username_or_password(self):
		username = ""
		password = ""
		#success,msg = self.remote.getUserToken(username,password)
		#self.assertFalse(success)

		username = ""
		password = ""
		#success,msg = self.remote.getUserToken(username,password)
		#self.assertFalse(success)

	def test_getUserToken_with_wrong_username(self):
		username = ""
		password = ""
		#success,msg = self.remote.getUserToken(username,password)
		#self.assertFalse(success)

	def test_getUserToken_with_wrong_password(self):
		username = ""
		password = ""
		#success,msg = self.remote.getUserToken(username,password)
		#self.assertFalse(success)

	def test_userPush(self):
		token = "4a7801150880a265cb803b9d144fd153"
		code = "Test code"
		name = "Test name"
		expire = PasteExpire.YEAR
		vis = PasteType.PRIVATE
		#self.remote.userPush(self.on_done,token,code,name,expire,vis)

	def test_userPush_wrong_token(self):
		token = "4a7801150880a265cb803b9d144fd"
		code = "Sample code 2"
		name = "Test name2"
		expire = PasteExpire.YEAR
		vis = PasteType.PRIVATE
		#self.remote.userPush(self.on_wrong_done,token,code,name,expire,vis)

	def on_wrong_done(self,data):
		success,msg = data
		print(msg)
		self.assertFalse(success)

	def test_userPush_empty_content(self):
		token = "4a7801150880a265cb803b9d144fd153"
		code = ""
		name = "Test name2"
		expire = PasteExpire.YEAR
		vis = PasteType.PRIVATE
		#self.remote.userPush(self.on_wrong_done,token,code,name,expire,vis)

	def test_userPush_wrong_type_argument(self):
		token = "4a7801150880a265cb803b9d144fd153"
		code = "sample code 23"
		name = "Test name2"
		expire = PasteExpire.YEAR
		vis = 1
		#self.remote.userPush(self.on_wrong_done,token,code,name,expire,vis)

	def test_getUserPasteList(self):
		token = "f06d910db7fbc3c007f011bac975651b"
		limit = "5"
		#self.remote.getUserPasteList(self.on_user_list,token,limit)

	def on_user_list(self,data):
		success,msg = data
		print(data)
		self.assertTrue(success)

	def test_getUserPasteList_Invalid_Token(self):
		token = "f06d910db7fbc3c007f011bac975651"
		limit = "5"
		#self.remote.getUserPasteList(self.on_user_list_error,token,limit)

	def on_user_list_error(self,data):
		success,msg = data
		self.assertFalse(success)

	def test_getUserPasteList_invalid_limit(self):
		token = "f06d910db7fbc3c007f011bac975651b"
		limit = "102000"
		#self.remote.getUserPasteList(self.on_user_list_error,token,limit)

	def test_getUserPasteList_different_type_token(self):
		#self.assertRaises(ValueError,self.list_different_type_token)
		pass 

	def list_different_type_token(self):
		token = 5221
		limit = "10"
		#self.remote.getUserPasteList(self.on_user_list_error,token,limit)

	def test_getUserPasteList_differenty_type_callable(self):
		#self.assertRaises(ValueError,self.list_different_type_callable)
		pass 

	def list_different_type_callable(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		limit = "10"
		#self.remote.getUserPasteList("self.on_user_list_error",token,limit)

	def test_getUserPasteList_empty_callable(self):
		#self.assertRaises(ValueError,self.list_empty_callable)
		pass 

	def list_empty_callable(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		limit = "10"
		#self.remote.getUserPasteList(None,token,limit)

	def test_getUserPasteList_different_type_limit(self):
		#self.assertRaises(ValueError,self.differentTypeLimit)
		pass 

	def differentTypeLimit(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		limit = 10
		#self.remote.getUserPasteList(self.on_user_list_error,token,limit)

	def test_getUserPaste(self):
		token = "f06d910db7fbc3c007f011bac975651b"
		paste_key = "6HaZsSay"
		#self.remote.getUserPaste(self.on_user_paste,token,paste_key)

	def on_user_paste(self,data):
		success,msg = data
		print(msg)
		self.assertTrue(success)

	def test_getUserPaste_invalid_paste_key(self):
		token = "f06d910db7fbc3c007f011bac975651b"
		paste_key = "allkhwa"
		#self.remote.getUserPaste(self.on_user_paste_wrong,token,paste_key)

	def on_user_paste_wrong(self,data):
		success,msg = data
		print(msg)
		self.assertFalse(success)

	def test_getUserPaste_invalid_token(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe"
		paste_key = "6HaZsSay"
		#self.remote.getUserPaste(self.on_user_paste_wrong,token,paste_key)

	def test_getUserPaste_empty_paste_key(self):
		pass 
		#self.remote.getUserPaste(self.on_user_paste_wrong,token,paste_key)	
		#self.assertRaises(ValueError,self.emptyPasteKey)

	def emptyPasteKey(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		paste_key = ""
		#self.remote.getUserPaste(self.on_user_paste_wrong,token,paste_key)

	def differentTypePaste(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		paste_key = 12344
		#self.remote.getUserPaste(self.on_user_paste_wrong,token,paste_key)

	def test_getUserPaste_different_type_paste_key(self):
		pass
		#self.assertRaises(ValueError,self.differentTypePaste)

	def test_getUserPaste_different_type_callable(self):
		pass
		#self.assertRaises(ValueError,self.differentTypeCallable)

	def differentTypeCallable(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		paste_key = 12344
		#self.remote.getUserPaste("self.on_user_paste_wrong",token,paste_key)

	def test_getUserPaste_empty_callable(self):
		#self.assertRaises(ValueError,self.emptyCallable)
		pass 

	def emptyCallable(self):
		token = "1923d360f82e7d6f3ac49450a2c95fe7"
		paste_key = "12344"
		#self.remote.getUserPaste(None,token,paste_key)

	def test_getPublicPaste(self):
		paste_key = "4gQCtbbj"
		self.remote.getPublicPaste(self.on_success_paste,paste_key)	

	def on_success_paste(self,data):
		success,msg = data
		print(msg)
		self.assertTrue(success)

	def test_getPublicPaste_empty_paste_key(self):
		#self.assertRaises(ValueError,self.getPublicPaste_empty_paste_key)
		pass 

	def getPublicPaste_empty_paste_key(self):
		paste_key = ""
		self.remote.getPublicPaste(self.on_error_paste,paste_key)

	def on_error_paste(self,data):
		success,msg = data
		print(msg)
		self.assertFalse(success)

	def test_getPublicPaste_wrong_paste_key(self):
		paste_key = "avwdaw23"
		#self.remote.getPublicPaste(self.on_error_paste,paste_key)


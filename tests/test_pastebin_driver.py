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
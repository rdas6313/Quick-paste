from unittesting import DeferrableTestCase
from Quick_Paste.utility import *

class TestUtility(DeferrableTestCase):

	def setUp(self):
		pass

	def test_get_key_from_url(self):
		url = "https://pastebin.com/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertEqual(key,actual_key)
		self.assertTrue(status)

	def test_get_key_from_url_wrong_url(self):
		url = "https://pastebi.com/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)


	def test_get_key_from_url_wrong_url2(self):
		url = "https://facebook.com/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)

	def test_get_key_from_url_wrong_url3(self):
		url = "https://pastebin.com/4gnN6fD3/"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)

	def test_get_key_from_url_wrong_url4(self):
		url = "https://pastebin.com/23/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)

	def test_get_key_from_url_wrong_url5(self):
		url = "https://www.pastebin.com/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)

	def test_get_key_from_url_wrong_url6(self):
		url = "www.pastebin.com/4gnN6fD3"
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		self.assertFalse(key)
		self.assertFalse(status)

	def test_get_key_from_url_empty_url(self):
		self.assertRaises(ValueError,self.get_key_from_url_empty_url)

	def get_key_from_url_empty_url(self):
		url = ""
		pattern = "https://pastebin.com/"
		actual_key = "4gnN6fD3"
		get_key_from_url(url,pattern)
		

	def test_get_key_from_url_empty_pattern(self):
		self.assertRaises(ValueError,self.get_key_from_url_empty_pattern)

	def get_key_from_url_empty_pattern(self):
		url = "https://pastebin.com/4gnN6fD3"
		pattern = ""
		actual_key = "4gnN6fD3"
		status,key = get_key_from_url(url,pattern)
		
from unittesting import DeferrableTestCase
from Quick_Paste.http import *
import json

class TestHttp(DeferrableTestCase):

	def setUp(self):
		self.http = HttpClient()

	def test_post(self):
		base_url = "jsonplaceholder.typicode.com"
		url_path = "/posts"
		payload = json.dumps({
			"title":"Raja",
			"body" : "Hey there! Its's Raja",
			"userId" : 1
		});

		headers = {
    		'Content-type': 'application/json; charset=UTF-8',
  		}

		response_code,msg = self.http.post(base_url,url_path,payload,headers)
		self.assertEqual(response_code,201)

	def test_post_wrong_data(self):
		base_url = "jsonplaceholder.typicode.com"
		url_path = "/posts"
		payload = json.dumps({
			"abcd":23
		});

		headers = None
		response_code,msg = self.http.post(base_url,url_path,payload,headers)
		self.assertNotEqual(response_code,201)

	def test_post_wrong_url(self):
		base_url = "jsonplaceholder.typicode.com"
		url_path = "/"
		payload = json.dumps({
			"title":"Raja",
			"body" : "Hey there! Its's Raja",
			"userId" : 1
		});

		headers = {
    		'Content-type': 'application/json; charset=UTF-8',
  		}
		response_code,msg = self.http.post(base_url,url_path,payload,headers)
		self.assertNotEqual(response_code,201)
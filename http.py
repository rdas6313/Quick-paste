from .logger import Logger
from http.client import *
import http.client as http_client

class HttpClient:

	__CLASS_NAME = "HttpClient"

	__LOG = Logger()

	def __init__(self):
		pass

	def post(self,base_url,path_url,payload,headers):
		conn = None
		res = None
		try:
			
			self.__LOG.info("{} Connecting to {}".format(self.__CLASS_NAME,base_url))
			conn = http_client.HTTPSConnection(base_url)
			self.__LOG.debug(payload)			
			conn.request("POST", path_url, payload, headers)
			res = conn.getresponse()
			res_data = res.read()
			data = res_data.decode("utf-8")
			self.__LOG.info("{} Response Code : {}".format(self.__CLASS_NAME,res.status))
			self.__LOG.info("{} Response Data : {}".format(self.__CLASS_NAME,data))
			
		except InvalidURL as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except NotConnected as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except CannotSendRequest as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except HTTPException as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except:
			self.__LOG.error("{} Unknown exception".format(self.__CLASS_NAME))
		finally:
			if conn:
				conn.close()
				self.__LOG.info("{} Connection is closed with {}".format(self.__CLASS_NAME,base_url))
			else:
				self.__LOG.error("{} Connection is null".format(self.__CLASS_NAME))
			if res:
				return (res.status,data)
			else:
				return (400,None)


	def get(self,base_url,path_url):
		conn = None 
		res = None 
		try:
			
			self.__LOG.info("{} Connecting to {}".format(self.__CLASS_NAME,base_url))
			conn = http_client.HTTPSConnection(base_url)
			conn.request("GET", path_url)
			res = conn.getresponse()
			res_data = res.read()
			data = res_data.decode("utf-8")
			
			self.__LOG.info("{} Response Code : {}".format(self.__CLASS_NAME,res.status))

		except InvalidURL as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except NotConnected as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except CannotSendRequest as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except HTTPException as e:
			self.__LOG.error("{} {}".format(self.__CLASS_NAME,e))
		except:
			self.__LOG.error("{} Unknown exception".format(self.__CLASS_NAME))
		finally:
			if conn:
				conn.close()
				self.__LOG.info("{} Connection is closed with {}".format(self.__CLASS_NAME,base_url))
			else:
				self.__LOG.error("{} Connection is null".format(self.__CLASS_NAME))
			if res:
				return (res.status,data)
			else:
				return (400,None)
import re
import os
import urllib
import urllib2
import httplib2
import Cookie
import oauth2 as oauth
import time, datetime, simplejson
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# Set up consumer key
consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

# Enable cookies
cookie_string = os.environ.get('HTTP_COOKIE')

# Create and sign an oauth request to retrieve data from Loggly
def auth_url(url, access_token):
	access_t = oauth.Token.from_string(access_token)
	h = httplib2.Http()
	signature_method = oauth.SignatureMethod_HMAC_SHA1()
	oauth_req4 = oauth.Request.from_consumer_and_token(consumer,
                                                       token=access_t,
                                                       http_url=url)
	oauth_req4.sign_request(signature_method, consumer, access_t)
	resp, jsonoutput = h.request(url, "GET", headers=oauth_req4.to_header())
        return json.dumps(json.loads(jsonoutput))

# Set URL to retrieve inputs from the API
def get_data(access_token, logglysub):
        url = 'http://'+logglysub+'.loggly.com/api/inputs/'
	return auth_url(url, access_token)

# Set URL to retrieve facets data from the API
def get_facets(access_token, logglysub, inputname, searchquery, starttime, endtime):
        url = 'http://'+logglysub+'.loggly.com/api/facets/date/?q=inputname:'+inputname+'&from='+starttime+'&until='+endtime
	return auth_url(url, access_token)

# Set URL to retrieve log data from the API
def get_stats(access_token, logglysub, inputname, searchquery, starttime, endtime):
        url = 'http://'+logglysub+'.loggly.com/api/search/?q=inputname:'+inputname+'%20AND%20isjson:true&from='+starttime+'&until='+endtime+'&rows=1000'
	return auth_url(url, access_token)

class stats(webapp.RequestHandler):
        def post(self):
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		access_token = self.request.get('access_token')
                logglysub = self.request.get('logglysub')
		inputname = self.request.get('inputname')
		searchquery = self.request.get('searchquery')
		starttime = self.request.get('starttime')
		endtime = self.request.get('endtime')
		self.response.out.write(get_stats(access_token, logglysub, inputname, searchquery, starttime, endtime))


class facets(webapp.RequestHandler):
	def post(self):
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
		access_token = self.request.get('access_token')
                logglysub = self.request.get('logglysub')
                inputname = self.request.get('inputname')
                searchquery = self.request.get('searchquery')
                starttime = self.request.get('starttime')
                endtime = self.request.get('endtime')
		self.response.out.write(get_facets(access_token, logglysub, inputname, searchquery, starttime, endtime))


class auth(webapp.RequestHandler):
      def get(self):
                self.response.out.write(open ('dashboard.html').read())
      def post(self):
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                logglysub = self.request.get('logglysub')
		access_token = self.request.get('access_token')
                #NEED TO AUTHENTICATE BY BLACK MAGIC
                self.response.out.write(get_data(access_token, logglysub))

class dashboard(webapp.RequestHandler):
     def get(self):
		self.response.out.write(open ('dashboard.html').read())

app = webapp.WSGIApplication([('/', auth),('/show', stats),('/grab', stats),('/grabf', facets),('/dashboard', dashboard)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

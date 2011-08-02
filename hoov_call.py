import re
import os
import urllib
import urllib2
import httplib2
import time, datetime, simplejson
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

def auth_url(url, user, passwd):
        realm = 'Loggly API'
	# create auth handler, build opener
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm=realm,
                                  uri=url,
                                  user=user,
                                  passwd=passwd)
        opener = urllib2.build_opener(auth_handler)
        # use opener to open the URL
        file_handler = opener.open(url)
        jsonoutput = file_handler.read()
        return json.dumps(json.loads(jsonoutput))

def get_data(logglyname, logglypass, logglysub):
        url = 'http://'+logglysub+'.loggly.com/api/inputs/'
	user = logglyname
        passwd = logglypass
 
	return auth_url(url, user, passwd)

def get_facets(logglyname, logglypass, logglysub, inputname, searchquery, starttime, endtime):
        url = 'http://'+logglysub+'.loggly.com/api/facets/date/?q=inputname:'+inputname+'&from='+starttime+'&until='+endtime+'&gap=%2B1DAY'
	user = logglyname
        passwd = logglypass

	return auth_url(url, user, passwd)

def get_stats(logglyname, logglypass, logglysub, inputname, searchquery, starttime, endtime):
        url = 'http://'+logglysub+'.loggly.com/api/search/?q=inputname:'+inputname+'%20AND%20isjson:true&from='+starttime+'&until='+endtime+'&rows=1000'
	user = logglyname
        passwd = logglypass

	return auth_url(url, user, passwd)

class stats(webapp.RequestHandler):
        def post(self):
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                logglyname = self.request.get('logglyname')
                logglypass = self.request.get('logglypass')
                logglysub = self.request.get('logglysub')
		inputname = self.request.get('inputname')
		searchquery = self.request.get('searchquery')
		starttime = self.request.get('starttime')
		endtime = self.request.get('endtime')
		self.response.out.write(get_stats(logglyname, logglypass, logglysub, inputname, searchquery, starttime, endtime))


class facets(webapp.RequestHandler):
	def post(self):
		self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                logglyname = self.request.get('logglyname')
                logglypass = self.request.get('logglypass')
                logglysub = self.request.get('logglysub')
                inputname = self.request.get('inputname')
                searchquery = self.request.get('searchquery')
                starttime = self.request.get('starttime')
                endtime = self.request.get('endtime')
		self.response.out.write(get_facets(logglyname, logglypass, logglysub, inputname, searchquery, starttime, endtime))


class auth(webapp.RequestHandler):
      def get(self):
                self.response.out.write(open ('dashboard.html').read())
      def post(self):
                self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
                logglyname = self.request.get('logglyname')
                logglypass = self.request.get('logglypass')
                logglysub = self.request.get('logglysub')
                #NEED TO AUTHENTICATE BY BLACK MAGIC
                self.response.out.write(get_data(logglyname, logglypass, logglysub))

class dashboard(webapp.RequestHandler):
     def get(self):
		self.response.out.write(open ('dashboard.html').read())

app = webapp.WSGIApplication([('/', auth),('/show', stats),('/grab', stats),('/grabf', facets),('/dashboard', dashboard)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

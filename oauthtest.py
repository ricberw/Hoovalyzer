import urlparse
import httplib2
import datetime
import oauth2 as oauth
import Cookie
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'

request_token_url = 'http://ricberw.loggly.com/api/oauth/request_token/'
access_token_url = 'http://ricberw.loggly.com/api/oauth/access_token/'
authorize_url = 'https://ricberw.loggly.com/api/oauth/authorize/'


def get_data():
    import Cookie
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    
    h = httplib2.Http()

    # get request token
    parameters = {}
    # We dont have a callback server, we're going to use the browser to
    # authorize.

    parameters['oauth_callback'] = 'http://localhost:8080/oauthreturned/'
    oauth_req1 = oauth.Request.from_consumer_and_token(
        consumer, http_url=request_token_url, parameters=parameters)
    oauth_req1.sign_request(signature_method, consumer, None)

    response, content = h.request(oauth_req1.to_url(), 'GET')
    token = oauth.Token.from_string(content)
    
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    c = Cookie.SimpleCookie()
    c['secret'] = str(token.secret)
    c['secret']["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    print c
    
    oauth_req2 = oauth.Request.from_token_and_callback(
        token=token, callback='http://localhost:8080/oauthreturned/', http_url=authorize_url)

    return oauth_req2.to_url()
    
class redirect(webapp.RequestHandler):
        def get(self):
                self.response.out.write(open ('redirect.html').read())

class auth(webapp.RequestHandler):
      def get(self):
                self.response.out.write(get_data())
            

app = webapp.WSGIApplication([('/oauthtest', auth),('/redirect', redirect)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
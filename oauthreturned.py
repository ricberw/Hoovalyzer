import time
import httplib2
import os
import urllib
import urllib2
import Cookie
import oauth2 as oauth
import gdata.docs.service
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


# Set global variables
consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'

# Set up the cookie string
cookie_string = os.environ.get('HTTP_COOKIE')

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

def get_access_token(req_t, verif, secret, logglysub):
    import urlparse
    import Cookie
    import datetime
    import oauth2 as oauth
    
    # Define the URL and access_token URL
    url = "http://"+logglysub+".loggly.com/api/inputs/"
    access_token_url = 'http://'+logglysub+'.loggly.com/api/oauth/access_token/'
    
    # Create an oauth token
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    token = oauth.Token(key = req_t, secret = secret)
    token.set_verifier(verif)
    
    oauth_req3 = oauth.Request.from_consumer_and_token(
        consumer, token=token, http_url=access_token_url)
    
    # Sign the oauth token
    oauth_req3.sign_request(signature_method, consumer, token)
    sign = oauth_req3.get_parameter('oauth_signature')
    
    # Send the oauth request for an access token
    response, content = h.request(oauth_req3.to_url(), 'GET')
    access_token = oauth.Token.from_string(content)

    # Send back the retrieved access token
    return access_token
    


def get_inputs(access_t, logglysub):
    import urlparse
    import Cookie
    import oauth2 as oauth
    
    # Define the URL and access_token URL
    url = "http://"+logglysub+".loggly.com/api/inputs/"
    access_token_url = 'http://'+logglysub+'.loggly.com/api/oauth/access_token/'
    
    # Sign the oauth request with the existing access token
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    oauth_req4 = oauth.Request.from_consumer_and_token(consumer,
                                                       token=access_t,
                                                       http_url=url)
    oauth_req4.sign_request(signature_method, consumer, access_t)
    resp, content = h.request(url, "GET", headers=oauth_req4.to_header())
    
    # Automatically redirect users to the correct page - and pass the access token        
    print 'Location: /?access_token='+urllib.quote(str(access_t))+'\n'
    
class oauth(webapp.RequestHandler):
    def get(self):
        # If there are no oauth params, user must have hit cancel - send back to the front page
        if self.request.get('oauth_verifier') == '':
            print 'Location: /\n'
        # If there are oauth params, generate an access token and save it
        else:
            url = self.request.arguments()
            oauth_v = self.request.get('oauth_verifier')
            req_token = self.request.get('oauth_token')
            req_secret = self.request.cookies['secret']
            logglysub = self.request.cookies['logglysub']
            access_token = get_access_token(req_token, oauth_v, req_secret, logglysub)
            
            json = (get_inputs(access_token, logglysub))
            return json

app = webapp.WSGIApplication([('/oauthreturned/', oauth)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
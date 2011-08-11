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


# Set the API endpoint 
url = "http://ricberw.loggly.com/api/inputs/"
consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'
access_token_url = 'http://ricberw.loggly.com/api/oauth/access_token/'

# Set the base oauth_* parameters along with any other parameters required
# for the API call.
cookie_string = os.environ.get('HTTP_COOKIE')

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
consumer = oauth.Consumer(key="MGueyfX4ZYdghpyMqU", secret="VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD")

def get_access_token(req_t, verif, secret):
    import urlparse
    import Cookie
    import oauth2 as oauth
    
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    token = oauth.Token(key = req_t, secret = secret)
    token.set_verifier(verif)
    
    oauth_req3 = oauth.Request.from_consumer_and_token(
        consumer, token=token, http_url=access_token_url)
    
    oauth_req3.sign_request(signature_method, consumer, token)
    
    sign = oauth_req3.get_parameter('oauth_signature')

    response, content = h.request(oauth_req3.to_url(), 'GET')
    access_token = oauth.Token.from_string(content)

    client = gdata.docs.service.DocsService()
    client.SetOAuthInputParameters(signature_method,consumer_key,consumer_secret=consumer_secret)

# the token key and secret should be recalled from your database
    client.SetOAuthToken(gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret))

    return access_token
    


def get_inputs(access_t):
    import urlparse
    import Cookie
    import oauth2 as oauth
    
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
    oauth_req4 = oauth.Request.from_consumer_and_token(consumer,
                                                       token=access_t,
                                                       http_url=url)
    oauth_req4.sign_request(signature_method, consumer, access_t)
    resp, content = h.request(url, "GET", headers=oauth_req4.to_header())
    content_dict = json.loads(content)
    num = len(content_dict)
    input_key = []
    input_name = []
    for i in range(num):
        if(content_dict[i]['service']['name'] =='HTTP'):
            input_key.append(content_dict[i]['input_token'])
            input_name.append(content_dict[i]['name'])
            
            
    print "<h1> %s </h1> " % 'YOU SUCK'
    for i in range(len(input_key)):
        print "<a href=\"javascript:(function(){newsrc=document.location.protocol+'//d3eyf2cx8mbems.cloudfront.net/js/loggly-0.1.0.js';document.body.appendChild(document.createElement('script')).src=newsrc;var logglykey='"+input_key[i]+"';var%20host=document.location.protocol+'//logs.loggly.com';function%20sendlog(host,logglykey){castor=new%20loggly({url:host+'/inputs/'+logglykey+'?rt=1',level:'log'});castor.log('url='+location.href);}function racecond(){try{loggly==null;sendlog(host,logglykey);}catch(err){setTimeout(racecond,100);}}setTimeout(racecond,100);})();\">Send to "+input_name[i]+"@loggly >></a><br>"
    
class oauth(webapp.RequestHandler):
    def get(self):
        url = self.request.arguments()
        oauth_v = self.request.get('oauth_verifier')
        req_token = self.request.get('oauth_token')
        req_secret = self.request.cookies['secret']
        access_token = get_access_token(req_token, oauth_v, req_secret)
        
        json = (get_inputs(access_token))
        return json 

app = webapp.WSGIApplication([('/oauthreturned/', oauth)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()
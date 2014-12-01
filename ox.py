#!/usr/bin/python
#
# Example code to authenticate against an Open-Xchange middleware based on
# http://oxpedia.org/wiki/index.php?title=HTTP_API#Module_.22token.22_.28since_7.4.0.29
# and request capabilities from the newly created session
# http://oxpedia.org/wiki/index.php?title=HTTP_API#Module_.22capabilities.22_.28available_with_v7.4.2.29
# 
# see 
# https://dev.ox.io/app-service-authentication-step-6/
# for more details
# 
# 
# usage example for http:
#
# oxc = ox.com_handler(params.getvalue('ox_token'), 'PUT_YOUR_SERVER_DOMAIN_HERE', 'THE-SECRET-IN-THE-FILE-tokenlogin-secrets', None)
# oxc.login()
# oxc.capabilities()
#
# usage example for https:
# 
# oxc = ox.com_handler(params.getvalue('ox_token'), 'PUT_YOUR_SERVER_DOMAIN_HERE', 'THE-SECRET-IN-THE-FILE-tokenlogin-secrets', 'https://')
# oxc.login()
# oxc.capabilities()
#
# Written by https://github.com/bishoph

import urllib2
import urllib
import uuid
import json
from cookielib import CookieJar

class com_handler:

 def __init__(self, ox_token, ox_server, secret, proto):
  self.ox_token = ox_token
  self.ox_server = ox_server
  self.client = 'Python-Redeem-Client-v0.1 '
  self.secret = secret
  if (proto != None):
   self.proto = proto
  else:
   self.proto = 'http://'
  self.ox_sessionid = None
  cj = CookieJar()
  self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
  self.opener.addheaders = [('User-Agent', self.client),]
  urllib2.install_opener(self.opener)

 def login(self):
  myuuid = uuid.uuid4()
  formdata = { "token" : self.ox_token, "client": self.client, "authId" : myuuid, "secret": self.secret }
  data_encoded = urllib.urlencode(formdata)
  request = urllib2.Request(url = self.proto + self.ox_server + '/ajax/login?action=redeemToken', data = data_encoded)
  f = urllib2.urlopen(request) 
  json_response = f.read()
  json_obj = json.loads(json_response)
  if (json_obj.has_key('session')):
   self.ox_sessionid = json_obj['session']
  
 def capabilities(self):
  if (self.ox_sessionid != None):
   request = urllib2.Request(url = self.proto + self.ox_server + '/ajax/capabilities?action=all&session='+self.ox_sessionid)
   f = urllib2.urlopen(request)
   print (f.read())
  else:
   print ('Got no sessionid!')
  


import httplib2
import os
import pycas
import binascii

from apiclient.discovery import build
from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.client import AccessTokenRefreshError
from google.appengine.api import memcache
from google.appengine.ext import webapp, db

OAUTH_CLIENT_SECRETS = """{
  "web": {
    "client_id": "[[INSERT CLIENT ID HERE]]",
    "client_secret": "[[INSERT CLIENT SECRET HERE]]",
    "redirect_uris": [],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}"""
OAUTH_PROVIDER = "https://www.googleapis.com/auth/plus.me"

#This is a base class that insures the user is authenticated
#before allowing them to access the rest of the class.
class session(webapp.RequestHandler):
    user={}
    
    def __init__(self, request, response):
        super(session, self).__init__(request, response)
        if "cid" in self.request.cookies and self.request.cookies["cid"] != "":
            cookie=self.request.cookies["cid"]
            user=memcache.get(cookie)
            #Is this session active?
            if user:
                self.user=user
                #Reset the server-side timeout value for this session.
                memcache.add(cookie,self.user,7200)
                #webapp.Request.cookies["cid"]
            #else:
            #    self.response.out.write("Doesn't work:"+str(self.request.cookies["cid"]))

    #Create a new session id and link it to a user account using memcachd
    #this should only be called after a sucessful login to prevent session fixation.
    def new_session(self, user):
        cookie=self.rand()
        sess={"email":user.email,
              "name":user.name,
              "id":str(user.key())}        
        #expires in two hours,  time in seconds. 
        memcache.add(cookie,sess,7200)
        #HttpOnly will help defend against XSS.
        self.response.headers.add_header("Set-Cookie", "cid="+cookie+"; path=/; HttpOnly")

    def destroy_session(self, user_id):
        #overwrite session id->user id mapping
        memcache.add(cookie,"",1)
        #null the cookie value
        self.response.headers.add_header("Set-Cookie", "cid=; path=/; HttpOnly")

    #generate a simple Cryptographic Nonce that is binary safe.
    def rand(self):
        #/dev/urandom is a very good entropy store
        #however this might not be /dev/urandom...
        r=os.urandom(24)
        r=binascii.hexlify(r)
        return r

class auth(session):

    def get(self):
        uni_key=self.request.path.split("/")[-1]
        l=db.GqlQuery("select * from Authentication where university=KEY(:1) limit 1",uni_key)
        l=l.fetch(1)[0]
        if l.cas_url:
            self.cas(l.cas_url,uni_key)
        elif l.oauth_url:
            self.oauth(l.oauth_url,l.oauth_client_id,l.oauth_client_id)

    #This is used to create a session.
    #First the user is authenticated using cas, 
    #then then they are mapped to a user
    #this mapping is stored using memcachd
    def cas(self,cas_url,university_key):
        SERVICE_URL = "http://localhost:9999/authentication/"+university_key
        status, id, cookie = pycas.login(cas_url, SERVICE_URL)
        if id:
          u=db.GqlQuery("select * from User where cas_id=:1",id)
          user=u.fetch(1)
          if len(user):
            user=user[0]
            #self.response.out.write("User logged in:<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            #a session id should only be created on successful login to prevent session fixation. 
            self.new_session(user)
            self.redirect("/")
          else:
            self.response.out.write("user not found,  new account?<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            #insert a new user:
            #datamodel.user(name=user.name,email="",cas_id=id).put()
            #ask the user for their email?
        

    #This is used to create a session.
    #First the user is authenticated using oauth, 
    #then then they are mapped to a user
    #this mapping is stored using memcachd
    #adapated from http://code.google.com/p/google-api-python-client/source/browse/samples/appengine/main.py
    def oauth(self,oauth_url,oauth_client_id,oauth_client_secret):  
        http = httplib2.Http(memcache)
        service = build("plus", "v1", http=http)
        decorator = oauth2decorator_from_clientsecrets(OAUTH_CLIENT_SECRETS,OAUTH_PROVIDER)      
        try:
            http = decorator.http()
            user = service.people().get(userId='me').execute(http)
            if user:
                u=db.GqlQuery("select * from user where oauth_id=:1",user)
                user=u.fetch(1)
                if len(user):
                    user=user[0]
                    self.response.out.write("User logged in:<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
                    #a session id should only be created on successful login to prevent session fixation. 
                    self.new_session(user)            
        except AccessTokenRefreshError:
            self.redirect('/')

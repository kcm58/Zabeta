import httplib2
import os
import pycas
import binascii
import datamodel
import sys
import pickle

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
    #Does this instance need authentication?
    always_allowed=False
    
    def __init__(self, request, response):
        super(session, self).__init__(request, response)
        #Check if this instance of session had disabled authentication
        if not self.always_allowed:
            if "cid" in self.request.cookies and self.request.cookies["cid"] != "":
                self.cookie=self.request.cookies["cid"]
                #Dont use memcache for anything else.
                #otherwise an attacker could read or delete an arbitrary value.
                user_mem=memcache.get(self.cookie)
                #Is this session active?
                if user_mem is not None and len(user_mem):
                    self.user=pickle.loads(user_mem)
                    #Reset the server-side timeout value for this session.
                    #return as fast as possible because this will affect all load times. 
                    memcache.set(self.cookie,user_mem,7200)
                    #webapp.Request.cookies["cid"]
                else:
                    #session expired
                    self.destroy_session()
                    sys.exit("Session expired")
                #   self.response.out.write("Doesn't work:"+str(self.request.cookies["cid"]))
            else:
                #Not allowed                  
                sys.exit("Not allowed")
    #Create a new session id and link it to a user account using memcachd
    #this should only be called after a successful login to prevent session fixation.
    def new_session(self, auth):
        user=auth.user
        cookie=self.rand()
        programs=[]
        tasks=[]
        #must be a string id
        for p in auth.programs:
            programs.append(str(p))
        for t in user.tasks:
            tasks.append(str(t))
        sess={"email":user.email,
              "full_name":user.full_name,
              "id":str(user.key()),
              "university":str(auth.university.key()),
              "programs":programs,
              "privileges":auth.privileges,
              "tasks":tasks}  
        sess_mem=pickle.dumps(sess)      
        #expires in two hours,  time in seconds. 
        memcache.set(cookie,sess_mem,7200)
        #HttpOnly will help defend against XSS.
        self.response.headers.add_header("Set-Cookie", "cid="+cookie+"; path=/; HttpOnly")

    def destroy_session(self):
        #overwrite session id->user id mapping
        memcache.delete(self.cookie)
        #null the cookie value
        self.response.headers.add_header("Set-Cookie", "cid=; path=/; HttpOnly")

    #generate a simple Cryptographic Nonce that is binary safe.
    def rand(self):
        #/dev/urandom is a very good entropy store
        #however this might not be /dev/urandom...
        r=os.urandom(24)
        r=binascii.hexlify(r)
        return r

class path_handler(webapp.RequestHandler):

    def get(self):
        uni_path=self.request.path.split("/")[-1].lower()
        l=datamodel.University.gql("where login_path=:1 limit 1",uni_path)
        uni_id=str(l.fetch(1)[0].key()) 
        self.redirect("/authentication/"+uni_id)

class auth(session):
    #The user doesn't need a session to access this class
    always_allowed=True

    def get(self):
        uni_key=self.request.path.split("/")[-1]
        l=datamodel.AuthenticationMethod.gql("where university=KEY(:1) limit 1",uni_key)
        l=l.fetch(1)
        if len(l):
            l=l[0]
            if l.cas_url:
                self.cas(l.cas_url,uni_key)
            elif l.oauth_url:
                self.oauth(l.oauth_url,l.oauth_client_id,l.oauth_client_id)
        else:
            #Looks like we don't have this university
            self.redirect("/")
            sys.exit()
    #This is used to create a session.
    #First the user is authenticated using cas, 
    #then then they are mapped to a user
    #this mapping is stored using memcachd
    def cas(self,cas_url,university_key):
        SERVICE_URL = "http://localhost:9999/authentication/"+university_key
        status, id, cookie = pycas.login(cas_url, SERVICE_URL)
        if id:
          ar=db.GqlQuery("select * from AuthenticationRecord where cas_id=:1",id)
          auth=ar.fetch(1)
          if len(auth):
            #self.response.out.write("User logged in:<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            #a session id should only be created on successful login to prevent session fixation. 
            self.new_session(auth[0])
            self.redirect("/")
          else:
            #TODO:  Looks like we need to create a user account
            #
            #user.name is not defined - line below causing "AttributeError: 'list' object has no attribute 'name'"
            #
            #self.response.out.write("user not found,  new account?<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            self.response.out.write("user not found, new account?<br />UID: "+str(id)+"<br />Cookie:"+str(cookie))
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
                u=db.GqlQuery("select * from User where oauth_id=:1",user)
                user=u.fetch(1)
                if len(user):
                    user=user[0]
                    self.response.out.write("User logged in:<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
                    #a session id should only be created on successful login to prevent session fixation. 
                    self.new_session(user)            
        except AccessTokenRefreshError:
            self.redirect('/')

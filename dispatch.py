import json
import pycas
import logging
import Cookie
import os
import binascii
import datamodel

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache

class session(webapp.RequestHandler):
    user_id=0
    
    def __init__(self, name, bases):
        super(session, self).__init__(name, bases)
        #u=datamodel.user(name="test",email="test@test.com",cas_id="rmb237")
        #u.put()
        if "cid" in self.request.cookies:
            cookie=self.request.cookies["cid"]
            user_id=memcache.get(cookie)
            #Is this session active?
            if user_id:
                self.user_id=user_id
                #Reset the server-side timeout value for this session.
                memcache.add(cookie,self.user_id,7200)
                self.response.out.write("works:"+str(self.request.cookies["cid"]))
                #webapp.Request.cookies["cid"]
            else:
                self.response.out.write("Doesn't work:"+str(self.request.cookies["cid"]))
        else:
            self.new_session("1")

    def new_session(self, user_id):
        cookie=self.rand()
        #expires in two hours,  time in seconds. 
        memcache.add(cookie,user_id,7200)
        self.response.headers.add_header("Set-Cookie", "cid="+cookie)

    #generate a simple Cryptographic Nonce that is binary safe.
    def rand(self):
        r=os.urandom(24)
        r=binascii.hexlify(r)
        return r

class dispatch(session):

    def get(self):
        self.dispatch()
        pass

    def post(self):
        self.dispatch()
        pass

    def dispatch(self):
        path=self.request.path.split("/")
        call_class=path[2]
        call_method=path[3]
        api = __import__("api.api")
        #Make sure the class in this API call is public:
        if api.LIBS.get(call_class):
            #pull up the class out of ./lib
            libs=api.LIBS.keys()
            mod = __import__('api.'+call_class,fromlist=libs)
            api_call=getattr(mod,call_class)
            instance = api_call(self.request)
            if instance.getPublic().get(call_method):
                #invoke the proper method based on the path
                ret=getattr(instance,call_method)()
            else:
                ret={"error":"invalid method"}
        else:
            ret={"error":"invalid class"}
        #format output:
        json_obj = json.dumps(ret)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_obj)

class index(session):

    def get(self):    
        index=open("client/index.html").read()
        self.response.out.write(index)
        pass

class cas(session):

    def get(self):
        CAS_SERVER  = "https://cas.nau.edu"
        SERVICE_URL = "http://localhost:9999/cas/"
        status, id, cookie = pycas.login(CAS_SERVER, SERVICE_URL)
        if id:
          u=db.GqlQuery("select * from user where cas_id=:1",id)
          user=u.fetch(1)
          if len(user):
            user=user[0]
            self.response.out.write("User logged in:<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            self.new_session(user.key())
          else:
            self.response.out.write("user not found,  new account?<br />Name: "+str(user.name)+"<br/>UID: "+str(id)+"<br />Cookie:"+str(cookie))
            #insert a new user:
            #datamodel.user(name=user.name,email="",cas_id=id).put()
            #ask the user for their email?

class o_auth(session):

    def get(self):
        self.response.out.write("This doesn't work yet!")
        
        

if __name__ == "__main__":    
    run_wsgi_app(webapp.WSGIApplication([('/', index),
                                         ('/cas/', cas),
                                         ('/oauth/', o_auth),
                                         ('/api/.*', dispatch)],
                                        debug=True))

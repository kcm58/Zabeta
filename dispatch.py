
import sys 
#Consolidate library files. 
sys.path.append("lib")

import json
import session
import moraapi
import datamodel

from google.appengine.ext import webapp, db
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import memcache, oauth
from mora.rest import RestDispatcher
import webapp2 as webapp

class dispatch(session.session):

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
            instance = api_call(self.request,self.response)
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

class index(session.session):

    def get(self):    
        index=open("client/index.html").read()
        self.response.out.write(index)

#A temp class used to populate the db with development data. 
class populate(session.session):

    def clear(self,model):
        query = model.all()
        entries = query.fetch(1000)
        db.delete(entries)

    def get(self):    
        #Clear all
        self.clear(datamodel.University)
        self.clear(datamodel.Authentication)
        self.clear(datamodel.User)
        self.clear(datamodel.Course)
        #debug,  create a new user
        u=datamodel.University(name="NAU",domain="nau.edu")
        u.put()       
        a=datamodel.Authentication(university=u.key(),cas_url="https://cas.nau.edu")
        a.put()
        # one user for each group member and advisor
        users = list([datamodel.User(name="Mike",email="test@test.com",cas_id="rmb237"),
                 datamodel.User(name="Jonah",email="test2@test.com",cas_id="jwh83"),
                 datamodel.User(name="Eddie",email="test3@test.com",cas_id="eh88"),
                 datamodel.User(name="Kyoko",email="test4@test.com",cas_id="kcm58"),
                 datamodel.User(name="Owain",email="test5@test.com",cas_id="olm3"),
                 datamodel.User(name="Eck",email="test6@test.com",cas_id="edo"),
                 datamodel.User(name="James",email="test7@test.com",cas_id="jdp85")])
        for r in users:
            r.put()
        c=datamodel.Course(program="NAU",numer="386",subject="CS",comment="This course is helpful.....")
        c.put()
        self.response.out.write("Ok!")

if __name__ == "__main__":
    RestDispatcher.setup('/mora', [moraapi.moratest])
 
    #app = webapp.WSGIApplication([('/', apitest.moratest),
    # RestDispatcher.route()], debug = True)
    t=RestDispatcher.route()
    run_wsgi_app(webapp.WSGIApplication([t,
                                         ('/', index),
                                         ('/authentication/.*', session.auth),                                         
                                         #('/cas', session.cas),
    #                                     ('/mora', apitest.moratest),
                                         ('/populate', populate),
                                         ('/api/.*', dispatch)
                                         ],
                                        debug=True))

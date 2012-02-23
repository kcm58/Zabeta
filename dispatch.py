
import sys 
#Consolidate library files. 
sys.path.append("lib")

import json
import session
import datamodel

from api import moraapi
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
        call_arg=False
        path=self.request.path.split("/")
        call_class=path[2]
        call_method=path[3]
        if len(path)>4:
          call_arg=path[4]
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
                if call_arg:
                    ret=getattr(instance,call_method)(call_arg)
                else:
                    ret=getattr(instance,call_method)()
                #We allow the user to return a GQL query and we'll convert it to json for them.
                if type(ret) is db.GqlQuery:
                    #1024 is always the max return size
                    u_list=ret.fetch(1024)
                    ret=[]
                    #iterate over each element returned by the select.
                    for u in u_list:
                        element={}
                        #iterate over each parameter specified in the select
                        for key in u._all_properties:
                            element[key]=getattr(u,key)
                        ret.append(element)
            else:
                ret={"error":"invalid method"}
        else:
            ret={"error":"invalid class"}
        #format output:    
        #call_class is needed for namespace
        json_obj = json.dumps({call_class:ret})
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
        self.clear(datamodel.AuthenticationRecord)
        self.clear(datamodel.User)
        self.clear(datamodel.Program)
        self.clear(datamodel.Course)
        #debug,  create a new user
        
        u=datamodel.University(name="NAU",domain="nau.edu",path="NAU")
        u.put()       
        #a=datamodel.AuthenticationMethod(university=u.key(),cas_url="https://cas.nau.edu")
        #a.put()
        # one user for each group member and advisor
        users = list([datamodel.User(name="Mike",email="test@test.com",cas_id="rmb237"),
                 datamodel.User(name="Jonah",email="test2@test.com",cas_id="jwh83"),
                 datamodel.User(name="Eddie",email="test3@test.com",cas_id="eh88"),
                 datamodel.User(name="Kyoko",email="test4@test.com",cas_id="kcm58"),
                 datamodel.User(name="Owain",email="test5@test.com",cas_id="olm3"),
                 datamodel.User(name="Eck",email="test6@test.com",cas_id="edo"),
                 datamodel.User(name="James",email="test7@test.com",cas_id="jdp85")])
        
        p=datamodel.Program(University=u,name="CS")
        p.put()
        for r in users:
            r.put()
        c=datamodel.Course(program=p,name="Embedded Systems",description="A cool course taught by Dr Palmer next semester",catalog="CS 499")
        c.put()
        self.response.out.write("Ok!")

if __name__ == "__main__":
    RestDispatcher.setup('/api/mora/course', [moraapi.course])
    c=RestDispatcher.route()
    RestDispatcher.setup('/api/mora/courseOffering', [moraapi.courseOffering])
    co=RestDispatcher.route()

    run_wsgi_app(webapp.WSGIApplication([c,
                                         co,
                                         ('/', index),
                                         ('/authentication/.*', session.auth),                                         
                                         #('/api/mora/.*', moraapi.moratest),
                                         ('/populate', populate),
                                         ('/api/.*', dispatch)
                                         ],
                                        debug=True))

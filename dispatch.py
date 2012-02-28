
import sys 
#Consolidate library files. 
sys.path.append("lib")

import json
import session
import datetime
import populate
import schedule

from api import crud
from google.appengine.ext import  db
from google.appengine.ext.webapp.util import run_wsgi_app
from mora.rest import RestDispatcher
import webapp2 as webapp

#Extend session so that we can enforce access control
class dispatch(session.session):

    def get(self):
        self.dispatch()

    def post(self):
        self.dispatch()

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
                            if True:
                                try:
                                    var=getattr(u,key)
                                except:
                                    pass
                                if type(var) is datetime.datetime:
                                    element[key]=var.isoformat("T") + "+00:00"
                                else:
                                    element[key]=str(var)
                            #except:
                            #    pass
                        ret.append(element)
            else:
                ret={"error":"invalid method"}
        else:
            ret={"error":"invalid class"}
        #format output:    
        #call_class is needed for namespace
        if call_class=="list":     
            #A special case so that the list returns the proper namespace
            #for the collection it is returning. 
            json_obj = json.dumps({call_method:ret})
        else:
            json_obj = json.dumps({call_class:ret})
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json_obj)

#A static page doesn't need to extend session
class index(webapp.RequestHandler):

    def get(self):    
        index=open("client/index.html").read()
        self.response.out.write(index)

if __name__ == "__main__":
    #try:
    RestDispatcher.setup('/api/mora', [crud.Course,crud.CourseOffering,crud.CourseTask,crud.Outcome,crud.User,crud.University])

    run_wsgi_app(webapp.WSGIApplication([RestDispatcher.route(),
                                         ('/', index),
                                         ('/authentication/.*', session.auth),
                                         ('/a/.*', session.path_handler),                                     
                                         #('/api/mora/.*', crud.moratest),
                                         ('/populate', populate.populate),
                                         ('/schedule', schedule.schedule),
                                         ('/api/.*', dispatch)
                                         ],
                                        debug=True))
    #except SystemExit:
    #  pass
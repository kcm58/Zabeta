import json 

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class dispatch(webapp.RequestHandler):
    
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

class index(webapp.RequestHandler):
    
    def get(self):
        index=open("index.html").read()
        self.response.out.write(index)
        pass

if __name__ == "__main__":
    run_wsgi_app(webapp.WSGIApplication([('/', index),
                                         ('/api/.*', dispatch)],
                                        debug=True))
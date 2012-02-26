from google.appengine.ext import webapp, db

class schedule(webapp.RequestHandler):

    def get(self):    
        self.response.out.write("run schedule")

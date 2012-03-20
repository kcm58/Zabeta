from google.appengine.ext import webapp, db
from dateutil.relativedelta import relativedelta
from google.appengine.api import mail
from types import *
import datamodel
import datetime
import dateutil

debug=1

class task_util(webapp.RequestHandler):
    
    def debug(self,message):
        global debug
        if debug==1:
            self.response.out.write(message)
            self.response.out.write("<br />")
            
    def get(self):
        cs_prog=datamodel.Program.gql("where name=:1","CS")
        cs_prog=cs_prog.fetch(1024)
        self.debug(cs_prog[0].name)
        
    def interpret(self,str,delta):
        self.debug("Do something")
        
task_util.interpret("str","str")
        
       
    
        
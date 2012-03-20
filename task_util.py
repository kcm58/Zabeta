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
        r_delta=relativedelta(months=+1)
        self.interpret_and_create("Every Six Months",r_delta,cs_prog[0])
        
    def interpret_and_create(self,str,delta,prog):
        school_year_model=datamodel.Semester.gql("where program=:1",prog)
        school_year_model.fetch(1024)
        for s in school_year_model:
            self.debug(s.name)
        
       
    
        
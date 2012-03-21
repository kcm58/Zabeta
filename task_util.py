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
        progs=datamodel.Program.gql("where name=:1","CS")
        progs=progs.fetch(1024)
        self.debug(progs[0].name)
        cs_prog=progs[0]
        
        #NOTE: To get delta, we could have user specify the date of start and subtract the number of days from then until now
        r_delta=relativedelta(months=+12) #This will be user specified
        
        term_dict=self.get_school_year_model(cs_prog)
        self.interpret("every fall;every spring;every winter;every 3 years;every year",r_delta,term_dict)
        
    def get_school_year_model(self,prog):
        
        school_year_model=datamodel.Semester.gql("where program=:1",prog)
        school_year_model.fetch(1024)
            
        #Build a dictionary with semester names as keys, and a list containing beginning and end dates as keys
        terms_dict={}
        for s in school_year_model:
            self.debug(s.name)
            self.debug(s.university)
            self.debug(s.begin_date)
            self.debug(s.end_date)
            terms_dict[s.name]=[s.begin_date,s.end_date]
            
        return terms_dict
    
    #NOTE: delta represents when to start the task
    def interpret(self,st,delta,term_dict):
        
        year_delta=relativedelta(months=+12)
        #Split on each statement
        cycle_str_els=st.split(";")
        
        for s in cycle_str_els:
            #Split each statement into words
            s_els=s.split(" ")
            if self.is_number(s_els[1])!=True:
                term_name=s_els[1]
                #Check to see if term exists
                if term_dict.has_key(term_name):
                    self.debug("Term: %s exists" %term_name)
                    term_dates=term_dict[term_name]
                    self.debug(term_dates)
                    new_begin_date=term_dates[0]+year_delta+delta
                    new_end_date=term_dates[1]+year_delta+delta
                    self.debug("New begin date: ")
                    self.debug(new_begin_date)
                    self.debug("New end date: ")
                    self.debug(new_end_date)
                
                    #TODO: Create the task including the delta
                    self.debug("We will create a new task here")
                else:
                    self.debug("Term: %s does not exist" %term_name)
            else:
                scalar=s_els[1]
                term_name=s_els[2]
                
            #self.debug(term_name)
            
    def is_number(self,s):
        try:
            float(s)
            return True
        except ValueError:
            return False

                       
#class Semester(db.MoraModel):
#    university = db.ReferenceProperty(University) #void pointer to university
#    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
#    begin_date = db.DateTimeProperty()
#    end_date = db.DateTimeProperty()
#    name = db.StringProperty()
        
       
    
        
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
        r_delta=relativedelta(months=+12)
        self.interpret_and_create("every fall;every spring;every winter;every 3 years;every year",r_delta,cs_prog[0])
        
    def interpret_and_create(self,str,delta,prog):
        #Get the semesters/terms for a school
        school_year_model=datamodel.Semester.gql("where program=:1",prog)
        school_year_model.fetch(1024)
            
        #Build a dictionary with semester names as keys and a list containing beginning and end dates as keys
        terms={}
        for s in school_year_model:
            self.debug(s.name)
            self.debug(s.university)
            self.debug(s.begin_date)
            self.debug(s.end_date)
            terms[s.name]=[s.begin_date,s.end_date]
        
        self.debug(terms)
        
        #Parse the string against the terms dict with the delta
        self.parse_cycle_str(str,delta,terms)
        
    def parse_cycle_str(self,str,delta,terms_dict):
        #Split on each statement
        cycle_str_els=str.split(";")
        
        for st in cycle_str_els:
            #Split each statement into words
            st_els=st.split(" ")
            if self.is_number(st_els[1])==True:
                scalar=st_els[1]
                term_name=st_els[2]
            else:
                term_name=st_els[1]
                
            #self.debug(term_name)
            
            #Check to see if term exists
            if terms_dict.has_key(term_name):
                self.debug("Term: %s exists" %term_name)
                term_dates=terms_dict[term_name]
                self.debug(term_dates)
                new_begin_date=term_dates[0]+delta
                new_end_date=term_dates[1]+delta
                self.debug("New begin date: ")
                self.debug(new_begin_date)
                self.debug("New end date: ")
                self.debug(new_end_date)
                
                #TODO: Create the task including the delta
                self.debug("We will create a new task here")
            else:
                self.debug("Term: %s does not exist" %term_name)
            
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
        
       
    
        
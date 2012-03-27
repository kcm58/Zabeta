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
        self.interpret("every fall",r_delta,term_dict)
        
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
    
    #Iterates over the school's term dates to determine the beginning of the school year
    def get_earliest_date(self,term_dict):
        
        year_delta=relativedelta(months=+12)
        earliest_date=datetime.datetime.now()+(2*year_delta)
        
        for t in term_dict:
            if t.begin_date<earliest_date:
                earliest_date=t.begin_date
                
        return earliest_date
    
    #Iterates over the school's term dates to determine the end of the school year
    def get_latest_date(self,term_dict):
        
        year_delta=relativedelta(months=+12)
        latest_date=datetime.datetime.now()-(2*year_delta)
        
        for t in term_dict:
            if t.end_date>latest_date:
                latest_date=t.end_date
                
        return latest_date
        
    #NOTE: delta represents when to start the task
    def interpret(self,st,delta,term_dict):
        
        year_delta=relativedelta(months=+12)
        curr_date=datetime.datetime.now().date()

        #Split each statement into words
        s_els=st.split(" ")
            
        if s_els[0]=="every" and self.is_number(s_els[1]==True): #E.G. "every 3 years"
            school_begin_date=self.get_earliest_date(term_dict) #Beginning of the school year
            school_end_date=self.get_latest_date(term_dict) #End of the school year
            self.debug("Beginning of school year: ")
            self.debug(school_begin_date)
            self.debug("End of school year: ")
            self.debug(school_end_date)
            scalar=s_els[1]
            new_begin_date=school_begin_date+(scalar*year_delta)
            new_end_date=school_end_date+(scalar*year_delta)
                      
        elif s_els[0]=="end" and self.is_number(s_els[2])==True: #E.G. "end of 3 years" 
            school_begin_date=self.get_earliest_date(term_dict) #Beginning of the school year
            school_end_date=self.get_latest_date(term_dict) #End of the school year
            self.debug("Beginning of school year: ")
            self.debug(school_begin_date)
            self.debug("End of school year: ")
            self.debug(school_end_date)
            scalar=s_els[2]
            new_begin_date=school_begin_date+(scalar*year_delta)
            new_end_date=school_end_date+(scalar*year_delta)
          
        elif (s_els[0]=="every" and self.is_number(s_els[1]!=True)) or (s_els[0]=="end" and self.is_number(s_els[2])!=True): #E.G. "every fall" or "end of fall"
            term_name=s_els[1]
            term_dates=term_dict[term_name]
            self.debug("Term dates: ")
            self.debug(term_dates)
            if curr_date > term_dates[0]: #We have already passed the date
                new_begin_date=term_dates[0]+year_delta+delta
                new_end_date=term_dates[1]+year_delta+delta
                self.debug("New begin date: ")
                self.debug(new_begin_date)
                self.debug("New end date: ")
                self.debug(new_end_date)
                
                #Return the new begin/end dates
                new_dates={}
                new_dates['begin_date']=new_begin_date
                new_dates['end_date']=new_end_date
                return new_dates
            else:
                new_begin_date=term_dates[0]+delta
                new_end_date=term_dates[1]+delta
                self.debug("New begin date: ")
                self.debug(new_begin_date)
                self.debug("New end date: ")
                self.debug(new_end_date)
                
        #Return the new begin/end dates
        new_dates={}
        new_dates['begin_date']=new_begin_date
        new_dates['end_date']=new_end_date
        return new_dates
                  
    #NOTE: delta represents when to start the task
    def interpret_old(self,st,delta,term_dict):
        
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
        
       
    
        
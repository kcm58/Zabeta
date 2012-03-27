from mora.rest import RestHandler,rest_create
from mora import db
import datamodel
import datetime

#A user is NOT revisioned,  and does not use version_interface
class User(RestHandler):
      
    model = datamodel.User
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)

#Authentication methods and and records are also not versioned        
class AuthenticationMethod(RestHandler):

    model = datamodel.AuthenticationMethod
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)

class AuthenticationRecord(RestHandler):

    model = datamodel.AuthenticationRecord
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)


class Outcome(RestHandler):

    model = datamodel.Outcome
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)
        #Override the base values. 
        self.params['program']=self.program_id
        self.params['university']=self.university_id
        new_outcome=datamodel.Outcome()
        new_outcome.from_json(self.params)
        #Populate the response
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)        

class Objective(RestHandler):

    model = datamodel.Objective
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)

    @rest_create("outcome")
    def response_new(self):
        #Override the base values. 
        self.params['program']=self.program_id
        self.params['university']=self.university_id
        new_outcome=datamodel.Outcome()
        new_outcome.from_json(self.params)
        #Populate the response
        self.model.outcomes.append(new_outcome)
        self.version_save(self.model)

class Task(RestHandler):

    model = datamodel.Task
    
    def show(self):
        self.response.out.write(self.model.to_json())
    
    def update(self):
        self.model.from_json(self.params)

    @rest_create("response")
    def response_new(self):
        #Populate the response
        self.model.response=str(self.params)
        self.model.save()

class AssessmentTask(Task):
  
    model = datamodel.AssessmentTask

class CourseTask(Task):
  
    model = datamodel.CourseTask 

class Course(RestHandler):

    model = datamodel.Course

    def show(self):
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class CourseOffering(RestHandler):

    model = datamodel.CourseOffering

    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)
        
class OutcomeSupport(RestHandler):

    model = datamodel.OutcomeSupport

    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)        
        
#A user is NOT revisioned,  and does not use version_interface
class Semseter(RestHandler):

    model = datamodel.Semester

    def show(self):
        self.response.out.write(self.model.to_json())

    def update(self):
        self.model.from_json(self.params)

class University(RestHandler):
    
    model = datamodel.University
      
    def show(self):
        self.response.out.write(self.model.to_json())
        
class Program(RestHandler):
      
    model = datamodel.Program
      
    def show(self):
        self.response.out.write(self.model.to_json())
        
class Minutes(RestHandler):

    model = datamodel.Minutes
    
    def show(self):
        self.response.out.write(self.model.to_json())
        
    def update(self):
        self.model.from_json(self.params)
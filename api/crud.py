from mora.rest import RestHandler,rest_create
from mora import db
import datamodel

class Outcome(RestHandler):

      model = datamodel.Outcome
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_json(self.params)

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
    
    def show(self):
        self.response.out.write(self.model.to_json())
    
    def update(self):
        self.model.from_json(self.params)

    @rest_create("response")
    def response_new(self):
        #Populate the response
        self.model.response=str(self.params)
        self.model.save()
        
class CourseTask(RestHandler):
  
    model = datamodel.CourseTask 
    
    def show(self):
        self.response.out.write(self.model.to_json())
    
    def update(self):
        self.model.from_json(self.params)

    @rest_create("response")
    def response_new(self):
        #Populate the response
        self.model.response=str(self.params)
        self.model.save() 

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

class User(RestHandler):
      
    model = datamodel.User
      
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
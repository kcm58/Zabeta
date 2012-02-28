from mora.rest import RestHandler,rest_create
from mora import db
from datamodel import *



class Outcome(RestHandler):

      model = Outcome
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_json(self.params)
              
class Task(RestHandler):

    model = Task
    
    def show(self):
        self.response.out.write(self.model.to_json())
    
    def update(self):
        self.model.from_json(self.params)

    @rest_create("response")
    def response_new(self):
        #Populate the response
        self.model.response="test"

class AssessmentTask(Task):
  
    model = AssessmentTask
    
class CourseTask(Task):
  
    model = CourseTask 
    
class Course(RestHandler):

    model = Course
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)

      
class CourseOffering(RestHandler):
      
    model = CourseOffering
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)
          
class User(RestHandler):
      
    model = User
      
    def show(self):
        self.response.out.write(self.model.to_json())
          
    def update(self):
        self.model.from_json(self.params)

class University(RestHandler):
      
    model = University
      
    def show(self):
        self.response.out.write(self.model.to_json())
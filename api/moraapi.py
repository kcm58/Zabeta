from mora.rest import RestHandler,rest_create
from mora import db
from datamodel import *



class outcome(RestHandler):

      model = Outcome
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_son(self.params)
              
class Task(RestHandler):

    model = Task
    
    def show(self):
        self.response.out.write(self.model.to_json())
    
    def update(self):
        self.model.from_son(self.params)   
       
    @rest_create("form")
    def form_new(self):
        #club = ClubModel()
        #self.model.response.
        club.from_json(self.params)   
                   
class course(RestHandler):
      
      model = Course
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_son(self.params)

      
class courseOffering(RestHandler):
      
      model = CourseOffering
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_son(self.params)

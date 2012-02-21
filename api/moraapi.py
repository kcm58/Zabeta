from mora.rest import RestHandler
from mora import db
from datamodel import *

      
class course(RestHandler):
      
      model = Course
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_son(self.params)
          
      def destroy(self):
          pass
      
class courseOffering(RestHandler):
      
      model = Course_Offering
      
      def show(self):
          self.response.out.write(self.model.to_json())
          
      def update(self):
          self.model.from_son(self.params)
          
      def destroy(self):
          pass
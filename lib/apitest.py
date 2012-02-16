from mora.rest import RestHandler
from mora import db
from datamodel import University


    
class moratest(RestHandler):
 
    model = University
 
    def show(self):
      self.response.out.write(self.model.to_json())
 
    def update(self):
      self.model.from_json(self.params)

    def destroy(self):
      self.model.from_json("TEST!")      
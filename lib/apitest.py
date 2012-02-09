from mora.rest import RestHandler
from mora import db


class MyUserModel(db.MoraModel):
 
    google_user = db.UserProperty()
 
    join_date = db.DateTimeProperty(auto_now_add=True)
    
class moratest(RestHandler):
 
    model = MyUserModel
 
    def show(self):
      self.respond.out.write(self.model.to_json())
 
    def update(self):
      self.model.from_json(self.params)

    def destroy(self):
      self.model.from_json("TEST!")      
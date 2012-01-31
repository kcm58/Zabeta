from google.appengine.ext import db

class outcome(db.Model):
  description = db.StringProperty()
  section = db.FloatProperty()
  
class course(db.Model):
  number = db.IntegerProperty()
  subject = db.StringProperty()
  term = db.StringProperty()
  #A faculty reference
  instructor = db.ReferenceProperty()
  
class assessment(db.Model):
  description = db.StringProperty()
  whenUtilized =  db.StringProperty()
  outcomes = db.ListProperty(db.ReferenceProperty())
  direct = db.BooleanProperty()

class measure(db.Model):
  description = db.StringProperty()

class student(db.Model):
  name = db.StringProperty()
  email = db.EmailProperty()
  
class faculty(db.Model):
  name = db.StringProperty()
  email = db.EmailProperty()

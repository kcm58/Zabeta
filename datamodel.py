from google.appengine.ext import db
  
class course(db.Model):
  number = db.IntegerProperty()
  subject = db.StringProperty()
  term = db.StringProperty()
  #A faculty reference
  instructor = db.ReferenceProperty()
  assessments = db.ListProperty(db.ReferenceProperty())

class assessment(db.Model):
  description = db.StringProperty()
  whenUtilized =  db.StringProperty()
  direct = db.BooleanProperty()
  outcomes = db.ListProperty(db.ReferenceProperty())
  survays = db.ListProperty(db.ReferenceProperty())
  rubrics = db.ListProperty(db.ReferenceProperty())

class outcome(db.Model):
  summary = db.StringProperty()
  description = db.StringProperty()
  section = db.FloatProperty()
  goals = db.ListProperty(db.StringProperty())

class survay(db.Model):
  description = db.StringProperty()

class rubric(db.Model):
  description = db.StringProperty()

class measure(db.Model):
  description = db.StringProperty()

class student(db.Model):
  name = db.StringProperty()
  email = db.EmailProperty()
  
class faculty(db.Model):
  name = db.StringProperty()
  email = db.EmailProperty()

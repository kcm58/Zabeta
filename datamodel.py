from google.appengine.ext import db
from mora import db
  
#Assign course_instance as a child of the proper course.
#class course_instance(db.Model):
#  term = db.StringProperty()
#  year = db.StringProperty()
#  abet_status = db.StringProperty()
#  #A faculty reference
#  instructor = db.ReferenceProperty()
#    
#class assessment(db.Model):
#  description = db.StringProperty()
#  whenUtilized =  db.StringProperty()
#  #direct/indirect
#  direct = db.BooleanProperty()
#  
#class course(db.Model):
#  number = db.IntegerProperty()
#  subject = db.StringProperty()
#  assessments = db.ListProperty(db.ReferenceProperty(assessment)
#  
#  
#class objective(db.Model):
#  description = db.StringProperty()
#  outcomes = db.ListProperty(db.ReferenceProperty())
#  
#class outcome(db.Model):
#  section = db.FloatProperty()
#  summary = db.StringProperty()
#  description = db.StringProperty()
#  goals = db.ListProperty(db.StringProperty())
#  assessments = db.ListProperty(db.ReferenceProperty())
#
#class measure(db.polymodel):
#  description = db.StringProperty()
#  
#class survay(measure):
#  description = db.StringProperty()
#
#class rubric(measure):
#  description = db.StringProperty()
#
#class CourseImprovementDocument(measure):
#  description = db.StringProperty()

class University(db.MoraModel):
  name = db.StringProperty(indexed=True)
  domain = db.StringProperty()
 
class Authentication(db.MoraModel):
  university = db.ReferenceProperty(University,indexed=True)
  oauth_url = db.StringProperty()
  oauth_client_id = db.StringProperty()
  oauth_client_secret = db.StringProperty()
  cas_url = db.StringProperty()

class User(db.MoraModel):
  name = db.StringProperty()
  email = db.EmailProperty()
  oauth_id = db.StringProperty()
  cas_id = db.StringProperty()
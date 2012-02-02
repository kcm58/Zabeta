from google.appengine.ext import db
  
class course(db.Model):
  number = db.IntegerProperty()
  subject = db.StringProperty()
  assessments = db.ListProperty(db.ReferenceProperty())

#Assign course_instance as a child of the proper course.
class course_instance(db.Model):
  term = db.StringProperty()
  year = db.StringProperty()
  abet_status = db.StringProperty()
  #A faculty reference
  instructor = db.ReferenceProperty()
    
class assessment(db.Model):
  description = db.StringProperty()
  whenUtilized =  db.StringProperty()
  #direct/indirect
  direct = db.BooleanProperty()
  
class objective(db.Model):
  description = db.StringProperty()
  outcomes = db.ListProperty(db.ReferenceProperty())
  
class outcome(db.Model):
  section = db.FloatProperty()
  summary = db.StringProperty()
  description = db.StringProperty()
  goals = db.ListProperty(db.StringProperty())
  assessments = db.ListProperty(db.ReferenceProperty())

class measure(db.polymodel):
  description = db.StringProperty()
  
class survay(measure):
  description = db.StringProperty()

class rubric(measure):
  description = db.StringProperty()

class CourseImprovementDocument(measure):
  description = db.StringProperty()

class user(db.polymodel):
  name = db.StringProperty()
  email = db.EmailProperty()
  
class student(user):
  priviledge = db.StringProperty(default="student")

class faculty(user):
  priviledge = db.StringProperty(default="faculty")

class admin(user):
  priviledge = db.StringProperty(default="admin")

###NOT SURE ABOUT: 
#programs in AuthenticationRecord: is it supposed to be program? NO
#reverse references?
#response is supposed to be a JSONString object in Task
#instrument instead of Rubric in CourseTask?
#in Outcome: intDays for evaluation_next and evauation_duration
#object reference in Version

from google.appengine.ext import db
from mora import db

class Object(db.MoraPolyModel):
    uid = db.StringProperty()
    
class Version(db.MoraPolyModel):
    commit_minor = db.IntegerProperty()
    commit_major = db.IntegerProperty()
    commit_timestamp = db.DateTimeProperty()
    commit_user = db.ReferenceProperty(None)#Reference to the User type
    commit_program = db.ReferenceProperty(None,indexed=True)#reference to the Program
    commit_object = db.ReferenceProperty(Object) 
    commit_commment = db.StringProperty()
    #This must be in all collections for access control.
    university = db.ReferenceProperty(None,indexed=True)
    
class Form(Version):
    form_name = db.StringProperty()
    where_from = db.StringProperty() #note: from is a keyword so use where_from
    require_attachments = db.StringListProperty()

class User(db.MoraModel):
    name = db.StringProperty()
    email = db.EmailProperty()
    
class University(Version):
    name = db.StringProperty()
    domain = db.StringProperty()
    semesters = db.StringProperty() #needs to be reverse reference
    path = db.StringProperty()
    programs = db.StringProperty() #needs to be reverse reference
    
class Program(Version):
    name = db.StringProperty()

class Task(Version):
    delegates = db.ListProperty(db.Key)
    name = db.StringProperty()
    begin_date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
    fulfilled = db.IntegerProperty()
    attachment_names = db.StringListProperty()
    attachment_blob_ids = db.StringListProperty()
    response = db.StringProperty() #Form resposne
 
class Course(Version):
    program = db.ReferenceProperty(Program,indexed=True)
    name = db.StringProperty()
    description = db.StringProperty()
    catalog = db.StringProperty()
    
class CourseTask(Task):
    course = db.ReferenceProperty(Course,indexed=True)
    rubric = db.ReferenceProperty(Task,indexed=True) 
    
class Semester(db.MoraModel):
    begin_date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
    name = db.StringProperty()
    university = db.ReferenceProperty(University)
    
class CourseOffering(Version):
    semester = db.ReferenceProperty(Semester)
    instructor = db.ReferenceProperty(User,indexed=True)
    student_count = db.IntegerProperty()
    section = db.StringProperty()
    course = db.ReferenceProperty(Course,indexed=True)
    final_grades = db.StringListProperty()
    tasks = db.StringListProperty() #needs to be reverse reference

class Instrument(Form):
    empty = db.StringProperty()   

class Outcome(Form):
    description = db.StringProperty()
    name = db.StringProperty()
    rationale = db.StringProperty()
    assessments = db.StringProperty() #needs to be reverse reference
    last_evaluation = db.DateTimeProperty()
    evaluation_next = db.IntegerProperty() #needs to be intDays
    evaluation_duration = db.IntegerProperty() #needs to be intDays
    rationalize_course = db.ListProperty(db.Key)
    rationalize_instrument = db.ReferenceProperty(Instrument,indexed=True)
    
class AssessmentTask(Task):
    outcome = db.ReferenceProperty(Outcome,indexed=True)
    
class Objective(Version):
    description = db.StringProperty()
    program = db.ReferenceProperty(Program,indexed=True)
    index = db.IntegerProperty()
    outcomes = db.ListProperty(db.Key)
    name = db.StringProperty()

class Minutes(Version):
    description = db.StringProperty()
    program = db.ReferenceProperty(Program)
    
class AuthenticationMethod(db.MoraModel):
    oauth_url = db.StringProperty()
    oauth_client_id = db.StringProperty()
    oauth_client_secret = db.StringProperty()
    cas_url = db.StringProperty()
    university = db.ReferenceProperty(University,indexed=True)
    
class AuthenticationRecord(db.MoraModel):
    oauth_id = db.StringProperty()
    cas_id = db.StringProperty()
    university = db.ReferenceProperty(University,indexed=True)
    programs = db.ListProperty(db.Key)#Progam refernce
    privileges = db.ListProperty(int)
    user = db.ReferenceProperty(User,indexed=True)

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
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
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
    #university = db.ReferenceProperty(None,indexed=True)
    
class Form(Version):
    form_name = db.StringProperty()
    assessment_form = db.StringProperty() 
    require_attachments = db.StringListProperty()
    description = db.StringProperty()
    instructions = db.StringProperty()
    
class ScheduleLog(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    timestamp = db.DateTimeProperty()
    task = db.ReferenceProperty(None,indexed=True) #void pointer to a task
    user = db.ReferenceProperty(None,indexed=True)
    email = db.EmailProperty()
    
class User(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    full_name = db.StringProperty() #full name
    display_name = db.StringProperty()
    email = db.EmailProperty()
    employee_id = db.StringProperty() #not end-user editible (admin only)
    phone_office = db.StringProperty()
    phone_personal = db.StringProperty()
    office = db.StringProperty()
    join_date = db.DateProperty()
    depart_date = db.DateProperty()
    thumbnail = db.StringProperty() #identifier of uploadable image
    webpage = db.StringProperty()
    tasks = db.ListProperty(db.Key) 
      
class University(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    name = db.StringProperty()
    domain = db.StringProperty()
    semesters = db.StringProperty() #needs to be reverse reference
    login_path = db.StringProperty() #this is an unclear name
    programs = db.StringProperty() #needs to be reverse reference
    thumbnail = db.StringProperty() #identifier of image file
    web_page = db.StringProperty()
    
class Program(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    name = db.StringProperty()
    university = db.ReferenceProperty(University,indexed=True)
    start_date = db.DateProperty() #null/blank for current?
    end_date = db.DateProperty() #null/blank for current?
    mission = db.StringProperty()
    description = db.StringProperty()
    webpage = db.StringProperty() #url to website
    thumbnail = db.StringProperty() #identifier of image file
    docs = db.StringProperty() #identifier of docs array
    nag_before = db.StringListProperty()
    nag_after = db.StringListProperty()

class Task(Version):
    delegates = db.ListProperty(db.Key)
    name = db.StringProperty()
    begin_date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
    fulfilled = db.IntegerProperty()
    attachment_names = db.StringListProperty()
    attachment_blob_ids = db.StringListProperty()
    response = db.StringProperty() #Form response

class TodoTask(Task):
    description = db.StringProperty()

class Course(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    program = db.ReferenceProperty(Program,indexed=True)
    name = db.StringProperty()
    description = db.StringProperty()
    catalog_descr = db.StringProperty() #ask Dr D about this
    catalog = db.StringProperty()
    webpage = db.StringProperty()
    core_topics = db.StringProperty()
 
class Instrument(Form):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program 
      
class CourseTask(Task):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(Program,indexed=True) #void pointer to program
    course = db.ReferenceProperty(Course,indexed=True)
    rubric = db.ReferenceProperty(Instrument,indexed=True) 
    
class Semester(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    begin_date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
    name = db.StringProperty()
    university = db.ReferenceProperty(University)
    
class CourseOffering(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    semester = db.ReferenceProperty(Semester)
    instructor = db.ReferenceProperty(User,indexed=True)
    student_count = db.IntegerProperty()
    section = db.IntegerProperty()
    course = db.ReferenceProperty(Course,indexed=True)
    final_grades = db.StringListProperty()
    tasks = db.StringListProperty() #needs to be reverse reference
    syllabus = db.StringProperty() #identifier of pdf file
    website = db.StringProperty()  

class Outcome(Form):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    outcome_description = db.StringProperty()
    name = db.StringProperty()
    rationale = db.StringProperty()
    assessments = db.ListProperty(db.Key) #needs to be reverse reference
    last_evaluation = db.DateTimeProperty()
    evaluation_next = db.IntegerProperty() #needs to be intDays
    evaluation_duration = db.IntegerProperty() #needs to be intDays
    rationalize_course = db.ListProperty(db.Key)
    rationalize_instrument = db.ReferenceProperty(Instrument,indexed=True)
    index = db.IntegerProperty()
    
class OutcomeSupport(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    course = db.ReferenceProperty(Course,indexed=True)
    instrument = db.ReferenceProperty(Instrument,indexed=True)
    rationale = db.StringProperty()
    goal = db.StringProperty()

class AssessmentTask(Task):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    outcome = db.ReferenceProperty(Outcome,indexed=True)
    
class Objective(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    description = db.StringProperty()
    program = db.ReferenceProperty(Program,indexed=True)
    index = db.IntegerProperty()
    outcomes = db.ListProperty(db.Key)
    name = db.StringProperty()

class Minutes(Version):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    description = db.StringProperty()
    program = db.ReferenceProperty(Program)
    docs = db.StringProperty() #identifier of docs array
    date = db.DateTimeProperty()
    content = db.StringProperty()
    attachment = db.StringProperty() # allow the user to upload a file.
    
class AuthenticationMethod(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    oauth_url = db.StringProperty()
    oauth_client_id = db.StringProperty()
    oauth_client_secret = db.StringProperty()
    cas_url = db.StringProperty()
    university = db.ReferenceProperty(University,indexed=True)
    
class AuthenticationRecord(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    oauth_id = db.StringProperty()
    cas_id = db.StringProperty()
    university = db.ReferenceProperty(University,indexed=True)
    programs = db.ListProperty(db.Key)#Progam refernce
    privileges = db.ListProperty(int)
    user = db.ReferenceProperty(User,indexed=True)
    
class EmailLog(db.MoraModel):
    university = db.ReferenceProperty(None,indexed=True) #void pointer to university
    program = db.ReferenceProperty(None,indexed=True) #void pointer to program
    task = db.ReferenceProperty(None,indexed=True) #void pointer to a task
    user = db.ReferenceProperty(None,indexed=True) #void pointer to a user
    email = db.StringProperty()
    
    
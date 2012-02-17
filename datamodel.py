from google.appengine.ext import db
from mora import db
  
class User(db.MoraModel):
    name = db.StringProperty()
    email = db.EmailProperty()
    oauth_id = db.StringProperty()
    cas_id = db.StringProperty()
    programs = db.StringProperty()
    privileges = db.IntegerProperty()
    university = db.StringProperty()

class Version(db.MoraPolyModel):
    minor = db.IntegerProperty()
    major = db.IntegerProperty()
    timestamp = db.DateTimeProperty()
    user = db.ReferenceProperty(User,indexed=True)
    
class University(db.MoraModel):
    name = db.StringProperty(indexed=True)
    domain = db.StringProperty()
 
class Authentication(db.MoraModel):
    university = db.ReferenceProperty(University,indexed=True)
    oauth_url = db.StringProperty()
    oauth_client_id = db.StringProperty()
    oauth_client_secret = db.StringProperty()
    cas_url = db.StringProperty()
    
class Program(db.MoraModel):
    university = db.StringProperty()
    name = db.StringProperty()
    
class Minutes(db.MoraModel):
    description = db.StringProperty()
    program = db.StringProperty()
    
class Course(db.MoraModel):
    comment = db.StringProperty()
    subject = db.StringProperty()
    number = db.IntegerProperty()
    outcomes = db.StringProperty()
    program = db.StringProperty()
    
class Course_Offering(db.MoraModel):
    term = db.StringProperty()
    year = db.IntegerProperty()
    instructor = db.ReferenceProperty(User,indexed=True)
    avg_grade = db.IntegerProperty()
    dfw_rate = db.IntegerProperty()
    student_count = db.IntegerProperty()
    cid = db.StringProperty()
    abet_status = db.IntegerProperty()
    section = db.IntegerProperty()
    course = db.StringProperty()
    
class Notification_Schedule(db.MoraModel):
    course_offering = db.StringProperty()
    assessment = db.StringProperty()
    start_time = db.DateTimeProperty()
    end_time = db.DateTimeProperty()
    delta_time = db.IntegerProperty()
    fulfilled = db.BooleanProperty()
    
class Outcome(db.MoraModel):
    description = db.StringProperty()
    name = db.StringProperty()
    rationale = db.StringProperty()
    courses = db.StringProperty()
    assessments = db.StringProperty()
    number = db.IntegerProperty()
    
class Assessment(db.MoraModel):
    description = db.StringProperty()
    rubric = db.StringProperty()
    course_eval = db.StringProperty()
    survey_uid = db.StringProperty()
    
class Rubric(db.MoraModel):
    reviewer_name = db.StringProperty()
    review_data = db.StringProperty()
    title = db.StringProperty()
    student_team_name = db.StringProperty()
    cs_course_deliverable_name = db.StringProperty()
    questions = db.StringProperty()
    overall_deliverable_eval = db.IntegerProperty()
    
class RubricQuestions(db.MoraModel):
    rating = db.IntegerProperty()
    knowledge_skill = db.StringProperty()
    unacceptable = db.StringProperty()
    meets = db.StringProperty()
    excees = db.StringProperty()
    
class Populated_Rubric(db.MoraModel):
    scores = db.ListProperty(db.Key)
    comments = db.ListProperty(db.Key)
    rubric = db.ReferenceProperty(Rubric,indexed=True)
    
class Populated_Survey(db.MoraModel):
    answers = db.ListProperty(db.Key)
    comments = db.ListProperty(db.Key)
    
class Choice(db.MoraModel):
    text = db.StringProperty()
    comment_flag = db.IntegerProperty()
    
class Choice_List(db.MoraModel):
    type_flag = db.IntegerProperty()
    choices = db.ListProperty(db.Key)
    
class Question(db.MoraModel):
    description = db.StringProperty()
    choices = db.ReferenceProperty(Choice_List)
    
class Survey_Question(db.MoraModel):
    questions = db.StringProperty()
    comment_flag = db.IntegerProperty()
    description = db.StringProperty()
    
class Survey(db.MoraModel):
    title = db.StringProperty()
    description = db.StringProperty()
    survey_questions = db.StringProperty()
    
class PopulatedSurvey(db.MoraModel):
    answers = db.ListProperty(db.Key)
    comments = db.ListProperty(db.Key)

class Course_Improvement_Suggestions(db.MoraModel):
    summarized_issue = db.StringProperty()
    source = db.StringProperty()
    implemented_response = db.StringProperty()
       
class CID(db.MoraModel):
    overview = db.StringProperty()
    course_name = db.StringProperty()
    semeseter = db.StringProperty()
    num_students_start = db.IntegerProperty()
    num_students_end = db.IntegerProperty()
    attrition_perc = db.IntegerProperty()
    prereq = db.StringProperty()
    coreq = db.StringProperty()
    instructor = db.StringProperty()
    num_a = db.IntegerProperty()
    num_b = db.IntegerProperty()
    num_c = db.IntegerProperty()
    num_d = db.IntegerProperty()
    num_f = db.IntegerProperty()
    outcomes = db.StringProperty()
    target_outcomes = db.ListProperty(db.Key)
    assessment = db.StringProperty()
    assessment_mechanisms = db.ListProperty(db.Key)
    outcomes_assessed = db.StringProperty()
    assessment_comments = db.StringProperty()
    outcomes_assessed = db.StringProperty()
    assessment_comments = db.StringProperty()
    assessment_data = db.StringProperty()
    assessment_data_comments = db.ListProperty(db.Key)
    course_improvement = db.StringProperty()
    improvement_suggestions = db.ReferenceProperty(Course_Improvement_Suggestions,indexed=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    



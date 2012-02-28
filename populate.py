import session
import datamodel
import datetime
from google.appengine.ext import db,webapp


#A temp class used to populate the db with development data. 
class populate(webapp.RequestHandler):

    def clear(self,model):
        query = model.all()
        entries = query.fetch(1024)
        db.delete(entries)

    def get(self):
        #Clear all
        self.clear(datamodel.University)
        self.clear(datamodel.AuthenticationRecord)
        self.clear(datamodel.User)
        self.clear(datamodel.Program)
        self.clear(datamodel.Course)
        self.clear(datamodel.Semester)
        self.clear(datamodel.CourseOffering)
        self.clear(datamodel.Task)
        self.clear(datamodel.CourseTask)
        self.clear(datamodel.Instrument)
        #debug,  create a new user
        
        u=datamodel.University(name="NAU",domain="nau.edu",path="nau")
        u.put()
        a=datamodel.AuthenticationMethod(university=u.key(),cas_url="https://cas.nau.edu")
        
        a.put()
        
        # one user for each group member and advisor
        
        p=datamodel.Program(University=u,name="CS")
        p.put()
        
        c1=datamodel.Course(program=p,name="Automata Theory",description="Finite and infinite models leading to an understanding of computability. ",catalog="CS 315")
        c1.put()
        c2=datamodel.Course(program=p,name="Principles of Languages",description="Abstract framework for understanding issues underlying all programming languages covering all four major paradigms.",catalog="CS 396")
        c2.put()
          
        i1=datamodel.User(name="Eck Doerry",email='coolguy@nau.edu')
        i2=datamodel.User(name="James Palmer",email='coolguy@nau.edu')
        i3=datamodel.User(name="Dieter Otte",email='coolguy@nau.edu')
        i4=datamodel.User(name="John Georgas",email='coolguy@nau.edu')
        i5=datamodel.User(name="Pat Kelly",email='coolguy@nau.edu')
        
        i1.put()
        i2.put()
        i3.put()
        i4.put()
        i5.put()
      
        s=datamodel.Semester(name="FALL11",university=u.key())
        s.put()
       
        co1=datamodel.CourseOffering(semester=s,instructor=i1,student_count=35,section="0001",course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])    
        co2=datamodel.CourseOffering(semester=s,instructor=i2,student_count=35,section="0001",course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])  
        co3=datamodel.CourseOffering(semester=s,instructor=i3,student_count=35,section="0001",course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])
        co4=datamodel.CourseOffering(semester=s,instructor=i4,student_count=35,section="0001",course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])
        co5=datamodel.CourseOffering(semester=s,instructor=i5,student_count=35,section="0001",course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])
        
        co1.put()
        co2.put()
        co3.put()
        co4.put()
        co5.put()
        
        
        #ct=datamodel.CourseTask(course=c1,rubric=t1)
        #ct.put()
        
        ins=datamodel.Instrument(name="Important Task Form",where_from="Your boss",require_attachments=["Course Eval"])
        ins.put()
        
        wiki_form="@name@;@description|textarea(5,10)@;@occupation|list(Scientist,Engineer,Philosopher)@"
        
        o2_1=datamodel.Outcome(name="Outcome 2.1: Ability to apply foundational theoretical concepts and skills related to algorithms and programs, including underlying knowledge of mathematics (including discrete math, linear algebra, and statistics)",
                            description="True competence in computer science requires not only the ability to apply known algorithms and data structures to solve a problem, but to innovatively and continually develop novel algorithms and data structures. Creating and verifying the efficiency and correctness of such novel abstractions implies a  solid understanding of theoretical foundations of computer science and mathematics",
                            rationale="Empty",
                            assessments="Empty",
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c1.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form)
        o2_1.put()
        
        o2_2=datamodel.Outcome(name="Outcome 2.2: Familiarity with a broad range of programming languages and paradigms, with practical competence in at least two languages and paradigms",
                            description="A competent computer scientist must not only possess practical competence in a number of specific computer languages, but must have a broad understanding of language paradigms, abstractions shared by all computer languages, and how computer languages related and compare to each other",
                            assessments="Empty",
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c2.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form)
        o2_2.put()
        #need assessments?
        
        #delegates=[i1.key(),i2.key(),i3.key(),i4.key(),i5.key()]
        
        course_tasks=[(datamodel.CourseTask(name="Collect student evals for CS315",begin_date=datetime.datetime(2011,12,1),end_date=datetime.datetime(2011,12,15),fulfilled=0),"315 Evals"),
                      (datamodel.CourseTask(name="Collect student evals for CS421",begin_date=datetime.datetime(2011,12,1),end_date=datetime.datetime(2011,12,15),fulfilled=0),"421 Evals"),
                      (datamodel.CourseTask(name="Collect student evals for CS249",begin_date=datetime.datetime(2011,12,1),end_date=datetime.datetime(2011,12,15),fulfilled=0),"249 Evals"),
                      (datamodel.CourseTask(name="Collect student evals for CS396",begin_date=datetime.datetime(2012,1,15),end_date=datetime.datetime(2012,5,15),fulfilled=0),"396 Evals"),
                      (datamodel.CourseTask(name="Collect student evals for CS200",begin_date=datetime.datetime(2011,12,1),end_date=datetime.datetime(2011,12,15),fulfilled=0),"200 Evals")]
                       
        users = [(datamodel.User(name="Mike",email="test@test.com"),"rmb237"),
                 (datamodel.User(name="Jonah",email="test2@test.com"),"jwh83"),
                 (datamodel.User(name="Eddie",email="test3@test.com"),"eh88"),
                 (datamodel.User(name="Kyoko",email="test4@test.com"),"kcm58"),
                 (datamodel.User(name="Owain",email="test5@test.com"),"olm3"),
                 (datamodel.User(name="Eck",email="test6@test.com"),"edo"),
                 (datamodel.User(name="James",email="test7@test.com"),"jdp85")]
        
        ct_key_list=[]
        usr_key_list=[]
        
        for ct,id in course_tasks:
            ct.put()
            ct_key_list.append(ct.key())
       
        for r,id in users:
            r.tasks=ct_key_list
            r.put()
            usr_key_list.append(r.key())
            #create an authentication record for each user. 
            ar=datamodel.AuthenticationRecord(university=u.key(),
                                           cas_id=id,
                                           user=r.key(),
                                           programs=[p.key()],
                                           privileges=[1])
            ar.put()
            
        for ct,id in course_tasks:
            ct.delegates=ct_key_list
            ct.put()
                       
        #c.put()
        self.response.out.write("Ok!")

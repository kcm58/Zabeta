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
        #debug, create a new user
        
        u=datamodel.University(name="NAU",domain="nau.edu",login_path="nau")
        u.put()
        a=datamodel.AuthenticationMethod(university=u.key(),cas_url="https://cas.nau.edu")
        a.put()
                
        p=datamodel.Program(University=u,name="CS")
        p.put()
        
        c1=datamodel.Course(program=p,name="Automata Theory",description="Finite and infinite models leading to an understanding of computability. ",catalog="CS 315")
        c1.put()
        c2=datamodel.Course(program=p,name="Principles of Languages",description="Abstract framework for understanding issues underlying all programming languages covering all four major paradigms.",catalog="CS 396")
        c2.put()
      
        s=datamodel.Semester(name="FALL11",university=u.key())
        s.put()

        ins=datamodel.Instrument(name="Important Task Form",where_from="Your boss",require_attachments=["Course Eval"])
        ins.put()
        
        wiki_form="@name@;@description|textarea(5,10)@;@occupation|list(Scientist,Engineer,Philosopher)@"
        
        o2_1=datamodel.Outcome(name="Outcome 2.1: Ability to apply foundational theoretical concepts and skills related to algorithms and programs, including underlying knowledge of mathematics (including discrete math, linear algebra, and statistics)",
                            description="True competence in computer science requires not only the ability to apply known algorithms and data structures to solve a problem, but to innovatively and continually develop novel algorithms and data structures. Creating and verifying the efficiency and correctness of such novel abstractions implies a solid understanding of theoretical foundations of computer science and mathematics",
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

        course_tasks=[(datamodel.CourseTask(name="Collect student evals for CS315",begin_date=datetime.datetime(2011,12,1),
                                            end_date=datetime.datetime(2011,12,15),fulfilled=0),"315 Evals"),
                      (datamodel.CourseTask(name="Collect student evals for CS396",begin_date=datetime.datetime(2011,12,1),
                                            end_date=datetime.datetime(2011,12,15),fulfilled=0),"421 Evals")]

        users = [(datamodel.User(full_name="Mike",email="test@test.com"),"rmb237"),
                 (datamodel.User(full_name="Jonah",email="test2@test.com"),"jwh83"),
                 (datamodel.User(full_name="Eddie",email="test3@test.com"),"eh88"),
                 (datamodel.User(full_name="Kyoko",email="test4@test.com"),"kcm58"),
                 (datamodel.User(full_name="Owain",email="test5@test.com"),"olm3"),
                 (datamodel.User(full_name="Eck",email="test6@test.com"),"edo"),
                 (datamodel.User(full_name="James",email="test7@test.com"),"jdp85")]
        
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
        
        course_offerings=[(datamodel.CourseOffering(semester=s,instructor=users[0][0].key(),student_count=35,section=1,
                                                        course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[1][0].key(),student_count=35,section=1,
                                                        course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[2][0].key(),student_count=35,section=2,
                                                        course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[3][0].key(),student_count=35,section=2,
                                                        course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[4][0].key(),student_count=35,section=3,
                                                        course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[5][0].key(),student_count=35,section=3,
                                                        course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[6][0].key(),student_count=35,section=4,
                                                        course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status']))]
        
        for co in course_offerings:
            co.put()
        
        for ct,id in course_tasks:
            ct.delegates=ct_key_list
            ct.put()
                       
        #c.put()
        self.response.out.write("Ok!")
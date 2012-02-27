import session
import datamodel
import datetime
from google.appengine.ext import db

#A temp class used to populate the db with development data. 
class populate(session.session):

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
        c=datamodel.Course(program=p,name="Automata Theory",description="Finite and infinite models leading to an understanding of computability. ",catalog="CS 315")
        c.put()
        i=datamodel.User(name="Dr Doerry",email='coolguy@nau.edu')
        i.put()
        s=datamodel.Semester(name="FALL11",university=u.key())
        s.put()
        co=datamodel.CourseOffering(semester=s,instructor=i,student_count=35,section="1111",course=c,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])
        co.put()
        t=datamodel.Task(delegates=[i.key()],name="Collect student evals for CS315",begin_date=datetime.datetime.now(),end_date=datetime.datetime.now(),fulfilled=0)
        t.put()
        ct=datamodel.CourseTask(course=c,rubric=t)
        ct.put()
        ins=datamodel.Instrument(name="Important Task Form",where_from="Your boss",require_attachments=["Course Eval"])
        ins.put()
        wiki_form="@name@;@description|textarea(5,10)@;@occupation|list(Scientist,Engineer,Philosopher)@"
        
        o=datamodel.Outcome(name="Outcome 2.1: Ability to apply foundational theoretical concepts and skills related to algorithms and programs, including underlying knowledge of mathematics (including discrete math, linear algebra, and statistics)",
                            description="True competence in computer science requires not only the ability to apply kown algorithms and data structures to solve a problem, but to innovatively and continually develop novel algorithms and data structures. Creating and verifying the efficiency and correctnss of such novel abstractions implies a solid understanding of theoretical foundations of computer science and mathematics",
                            rationale="Empty",
                            assessments="Empty",
                            last_evaluation=datetime.datetime.now(),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form)
        o.put()
        #need assessments?
          
        users = [(datamodel.User(name="Mike",email="test@test.com"),"rmb237"),
                 (datamodel.User(name="Jonah",email="test2@test.com"),"jwh83"),
                 (datamodel.User(name="Eddie",email="test3@test.com"),"eh88"),
                 (datamodel.User(name="Kyoko",email="test4@test.com"),"kcm58"),
                 (datamodel.User(name="Owain",email="test5@test.com"),"olm3"),
                 (datamodel.User(name="Eck",email="test6@test.com"),"edo"),
                 (datamodel.User(name="James",email="test7@test.com"),"jdp85")]

        for r,id in users:
            r.put()
            #create an authentication record for each user. 
            ar=datamodel.AuthenticationRecord(university=u.key(),
                                           cas_id=id,
                                           user=r.key(),
                                           programs=[p.key()],
                                           privileges=[1])
            ar.put()
            
        c.put()
        self.response.out.write("Ok!")

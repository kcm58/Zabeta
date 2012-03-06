import session
import datamodel
import datetime
from google.appengine.ext import db,webapp
import datetime
import dateutil
from dateutil.relativedelta import relativedelta


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
        
        u=datamodel.University(name="NAU",domain="nau.edu",login_path="nau",webpage="http://nau.edu")
        u.put()
        a=datamodel.AuthenticationMethod(university=u.key(),cas_url="https://cas.nau.edu")
        a.put()
                
        p=datamodel.Program(University=u,name="CS",start_date=datetime.date(1901,1,15),end_date=None,mission="To build an army of amazing computer scientists",
                            description="Computer Science program at NAU")
        p.put()
        
        c1=datamodel.Course(program=p,name="Automata Theory",description="Finite and infinite models leading to an understanding of computability. ",
                            core_topics="fundamental principles of computability and different families of languages.",
                            webpage="http://nau.edu/CEFNS/Engineering/Computer-Science/Welcome/",catalog="CS 315")
        c1.put()
        c2=datamodel.Course(program=p,name="Principles of Languages",description="Abstract framework for understanding issues underlying all programming languages covering all four major paradigms.",
                            core_topics="functional programming and underlying linguistic principles, constructs, and mechanisms associated with diverse programming paradigms",
                            webpage="http://nau.edu/CEFNS/Engineering/Computer-Science/Welcome/",catalog="CS 396")
        c2.put()
      
        s=datamodel.Semester(name="FALL11",university=u.key())
        s.put()

        ins=datamodel.Instrument(name="Important Task",assessment_form="Empty Assessment form",description="You need to complete this task...",
                                 instructions="Your mission, should you choose to accept it...",require_attachments=["Course Eval"])
        ins.put()
        
        wiki_form="@name@;@description|textarea(5,10)@;@occupation|list(Scientist,Engineer,Philosopher)@"
        
        o2_1=datamodel.Outcome(name="Outcome 2.1: Ability to apply foundational theoretical concepts and skills related to algorithms and programs, including underlying knowledge of mathematics (including discrete math, linear algebra, and statistics)",
                            index=1,
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
                            index=2,
                            description="A competent computer scientist must not only possess practical competence in a number of specific computer languages, but must have a broad understanding of language paradigms, abstractions shared by all computer languages, and how computer languages related and compare to each other",
                            assessments="Empty",
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c2.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form)
        o2_2.put()
        #kdjfhdkjhf
        
        
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=relativedelta(months=+1)
        deltas['six months']=relativedelta(months=+6)
        
        test_date_six_months=(datetime.datetime.now())-deltas['six months']
        test_date_month=(datetime.datetime.now())-deltas['month']
        test_date_week=(datetime.datetime.now())-deltas['week']
        test_date_day=(datetime.datetime.now())-deltas['day']
        
        course_tasks=[(datamodel.CourseTask(name="CS 315 Evals",description="Collect student evals for CS 315",begin_date=datetime.datetime(2012,1,1),
                                            end_date=datetime.datetime(2012,6,15),fulfilled=0),"315 Evals"),
                      (datamodel.CourseTask(name="CS 396 Evals",description="Collect student evals for CS396",begin_date=datetime.datetime(2012,1,1),
                                            end_date=datetime.datetime(2012,6,15),fulfilled=0),"396 Evals"),
                      (datamodel.CourseTask(name="Test six months before",description="Collect student evals for CS396",begin_date=test_date_six_months,
                                            end_date=test_date_six_months,fulfilled=0),"396 Evals"),
                      (datamodel.CourseTask(name="Test one month before",description="Collect student evals for CS396",begin_date=test_date_month,
                                            end_date=test_date_month,fulfilled=0),"396 Evals"),
                      (datamodel.CourseTask(name="Test one week before",description="Collect student evals for CS396",begin_date=test_date_week,
                                            end_date=test_date_week,fulfilled=0),"396 Evals"),
                      (datamodel.CourseTask(name="Test one day before",description="Collect student evals for CS396",begin_date=test_date_day,
                                            end_date=test_date_day,fulfilled=0),"396 Evals")]
                       
        users = [(datamodel.User(full_name="Michael Brooks",email="test@test.com",employee_id="rmb237",display_name="Mike",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"rmb237"),
                 (datamodel.User(full_name="Jonah Hirsch",email="test2@test.com",employee_id="jeh83",display_name="Jonah",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"jwh83"),
                 (datamodel.User(full_name="Eddie Hillenbrand",email="test3@test.com",employee_id="eh88",display_name="Eddie",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"eh88"),
                 (datamodel.User(full_name="Kyoko Makino",email="test4@test.com",employee_id="kcm58",display_name="Kyoko",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"kcm58"),
                 (datamodel.User(full_name="Owain Moss",email="test5@test.com",employee_id="olm3",display_name="Owain",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"olmm3"),
                 (datamodel.User(full_name="Eck Doerry",email="test6@test.com",employee_id="edo",display_name="Eck",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"edo"),
                 (datamodel.User(full_name="James Palmer",email="test7@test.com",employee_id="jdp85",display_name="James",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"jdp85")]
        
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
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[1][0].key(),student_count=35,section=1,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[2][0].key(),student_count=35,section=2,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[3][0].key(),student_count=35,section=2,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[4][0].key(),student_count=35,section=3,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[5][0].key(),student_count=35,section=3,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(semester=s,instructor=users[6][0].key(),student_count=35,section=4,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status']))]
        
        for co in course_offerings:
            co.put()
        
        for ct,id in course_tasks:
            ct.delegates=usr_key_list
            ct.put()
                       
        #c.put()
        self.response.out.write("Ok!")
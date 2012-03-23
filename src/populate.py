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
        self.clear(datamodel.Objective)
        #debug, create a new user
        
        u=datamodel.University(name="NAU",domain="nau.edu",login_path="nau",webpage="http://nau.edu")
        u.put()
        a=datamodel.AuthenticationMethod(university=u.key(),cas_url="https://cas.nau.edu")
        a.put()
        
        nag_before_dict=["six months before","one month before","one week before","one day before"]
        nag_after_dict=["six months after","one month after","one week after","one day after"]
                
        p=datamodel.Program(university=u,name="CS",start_date=datetime.date(1901,1,15),end_date=None,mission="To build an army of amazing computer scientists",
                            nag_before=nag_before_dict,nag_after=nag_after_dict,description="Computer Science")
        p.put()
        p.program=p.key()
        p.save()
        
        p2=datamodel.Program(university=u,name="EE",start_date=datetime.date(1901,1,15),end_date=None,mission="To build an army of amazing electrical engineers",
                            nag_before=nag_before_dict,nag_after=nag_after_dict,description="Electrical Engineering")
        p2.put()
        p2.program=p2.key()
        p2.save()
        
        p3=datamodel.Program(university=u,name="ME",start_date=datetime.date(1901,1,15),end_date=None,mission="To build an army of amazing mechanical engineers",
                            nag_before=nag_before_dict,nag_after=nag_after_dict,description="Mechanical Engineering")
        p3.put()
        p3.program=p3.key()
        p3.save()
        
        nau_semesters=[(datamodel.Semester(university=u,program=p,begin_date=datetime.datetime(2012,8,15),end_date=datetime.datetime(2012,12,15),name="fall")),
                       (datamodel.Semester(university=u,program=p,begin_date=datetime.datetime(2012,12,18),end_date=datetime.datetime(2013,1,12),name="winter")),
                       (datamodel.Semester(university=u,program=p,begin_date=datetime.datetime(2013,1,15),end_date=datetime.datetime(2013,5,12),name="spring")),
                       (datamodel.Semester(university=u,program=p,begin_date=datetime.datetime(2013,5,15),end_date=datetime.datetime(2013,8,12),name="summer")),
                       (datamodel.Semester(university=u,program=p,begin_date=datetime.datetime(2012,8,15),end_date=datetime.datetime(2013,8,15),name="year"))]
        for s in nau_semesters:
            s.put()
        
        c1=datamodel.Course(program=p,name="Automata Theory",description="Finite and infinite models leading to an understanding of computability. ",
                            core_topics="fundamental principles of computability and different families of languages.",
                            webpage="http://nau.edu/CEFNS/Engineering/Computer-Science/Welcome/",catalog="CS 315",
                            university=u.key())
        c1.put()
        c2=datamodel.Course(program=p,name="Principles of Languages",description="Abstract framework for understanding issues underlying all programming languages covering all four major paradigms.",
                            core_topics="functional programming and underlying linguistic principles, constructs, and mechanisms associated with diverse programming paradigms",
                            webpage="http://nau.edu/CEFNS/Engineering/Computer-Science/Welcome/",catalog="CS 396",
                            university=u.key())
        c2.put()
        c3=datamodel.Course(program=p2,name="EE 101",description="EE 101 Descrip",
                            core_topics="EE 101 Topics",
                            webpage="http://nau.edu/cefns/engineering/electrical/",catalog="EE 101",
                            university=u.key())
        c3.put()
        c4=datamodel.Course(program=p3,name="ME 101",description="ME 101 Descrip",
                            core_topics="ME 101 Topics",
                            webpage="http://nau.edu/cefns/engineering/mechanical/",catalog="ME 101",
                            university=u.key())
        c4.put()
      
        s=datamodel.Semester(name="FALL11",university=u.key())
        s.put()

        ins=datamodel.Instrument(name="Important Task",assessment_form="Empty Assessment form",description="You need to complete this task...",
                                 instructions="Your mission, should you choose to accept it...",require_attachments=["Course Eval"])
        ins.put()
        
        wiki_form="@name@;@description|textarea(5,10)@;@occupation|list(Scientist,Engineer,Philosopher)@"
        
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=relativedelta(months=+1)
        deltas['six months']=relativedelta(months=+6)
        
        test_date_day_of=datetime.datetime.now()
        
        test_date_six_months_before=(datetime.datetime.now())+deltas['six months']
        test_date_month_before=(datetime.datetime.now())+deltas['month']
        test_date_week_before=(datetime.datetime.now())+deltas['week']
        test_date_day_before=(datetime.datetime.now())+deltas['day']
        
        test_date_six_months_after=(datetime.datetime.now())-deltas['six months']
        test_date_month_after=(datetime.datetime.now())-deltas['month']
        test_date_week_after=(datetime.datetime.now())-deltas['week']
        test_date_day_after=(datetime.datetime.now())-deltas['day']
        
        course_tasks=[(datamodel.CourseTask(name="CS 315 Evals",description="Collect student evals for CS 315",begin_date=datetime.datetime(2012,1,1),
                                            end_date=datetime.datetime(2012,6,15),fulfilled=0,university=u.key()),"315 Evals"),
                      (datamodel.CourseTask(name="CS 396 Evals",description="Collect student evals for CS396",begin_date=datetime.datetime(2012,1,1),
                                            end_date=datetime.datetime(2012,6,15),fulfilled=0,university=u.key()),"396 Evals"),
                      (datamodel.CourseTask(name="Test six months before",description="Running the six month before test for scheduling",begin_date=test_date_six_months_before,
                                            end_date=test_date_six_months_before,fulfilled=0,university=u.key()),"Six month before test"),
                      (datamodel.CourseTask(name="Test one month before",description="Running the one month before test for scheduling",begin_date=test_date_month_before,
                                            end_date=test_date_month_before,fulfilled=0,university=u.key()),"One month before test"),
                      (datamodel.CourseTask(name="Test one week before",description="Running the one week before test for scheduling",begin_date=test_date_week_before,
                                            end_date=test_date_week_before,fulfilled=0,university=u.key()),"One week before test"),
                      (datamodel.CourseTask(name="Test one day before",description="Running the one day before test for scheduling",begin_date=test_date_day_before,
                                            end_date=test_date_day_before,fulfilled=0,university=u.key()),"One day before test"),
                      (datamodel.CourseTask(name="Test six months after",description="Running the six month after test for scheduling",begin_date=test_date_six_months_after,
                                            end_date=test_date_six_months_after,fulfilled=0,university=u.key()),"Six month after test"),
                      (datamodel.CourseTask(name="Test one month after",description="Running the one month after test for scheduling",begin_date=test_date_month_after,
                                            end_date=test_date_month_after,fulfilled=0,university=u.key()),"One month after test"),
                      (datamodel.CourseTask(name="Test one week after",description="Running the one week after test for scheduling",begin_date=test_date_week_after,
                                            end_date=test_date_week_after,fulfilled=0,university=u.key()),"One week after test"),
                      (datamodel.CourseTask(name="Test one day after",description="Running the one day after test for scheduling",begin_date=test_date_day_after,
                                            end_date=test_date_day_after,fulfilled=0,university=u.key()),"One day after test"),
                      (datamodel.CourseTask(name="Test day of",begin_date=test_date_day_of,
                                            end_date=test_date_day_of,fulfilled=0,university=u.key()),"One day after test")]
                       
        users = [(datamodel.User(full_name="Michael Brooks",email="rmb237@nau.edu",employee_id="rmb237",display_name="Mike",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"rmb237"),
                 (datamodel.User(full_name="Jonah Hirsch",email="jwh83@nau.edu",employee_id="jwh83",display_name="Jonah",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"jwh83"),
                 (datamodel.User(full_name="Eddie Hillenbrand",email="eh88@nau.edu",employee_id="eh88",display_name="Eddie",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"eh88"),
                 (datamodel.User(full_name="Kyoko Makino",email="kcm58@nau.edu",employee_id="kcm58",display_name="Kyoko",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"kcm58"),
                 (datamodel.User(full_name="Owain Moss",email="olm3@nau.edu",employee_id="olm3",display_name="Owain",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"olmm3"),
                 (datamodel.User(full_name="Eck Doerry",email="olm3@nau.edu",employee_id="edo",display_name="Eck",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"edo"),
                 (datamodel.User(full_name="James Palmer",email="olm3@nau.edu",employee_id="jdp85",display_name="James",
                                 phone_office="(928)555-5555",phone_personal="(928)666-6666"),"jdp85")]
        
        ct_key_list=[]
        usr_key_list=[]
        
        for ct,id in course_tasks:
            ct.program=p
            #self.response.out.write(ct.program.key())
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
                                           programs=[p.key(),p2.key(),p3.key()],
                                           privileges=[1,2,1])
            ar.put()
        
        o1_1=datamodel.Outcome(name="Possess professional skills and knowledge of the software design process",
                            index=1,
                            objective_index=1,
                            description="The distinguishing skill between a gifted programmer and a software engineer is that, in addition to strong program implementation skills, the software engineer has a strong background in design (i.e., the creative process of analyzing end-user problems and arriving at a robust conceptual solution) and extensive knowledge of formal design and build process (i.e., modern software engineering tools and techniques aimed at reliably transforming a design into a finished product).  This outcome seeks to evaluate the extent to which graduates achieve this distinction as true software engineers.",
                            rationale="Empty",
                            assessments=[ct_key_list[0]],
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c1.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form,
                            university=u.key())
        o1_1.put()
        
        o1_2=datamodel.Outcome(name="Ability to function effectively in both co-located and distributed software development teams.",
                            index=2,
                            objective_index=1,
                            description="This outcome reflects the fact that modern software engineering is rarely a solo effort; most software development efforts involve highly-coordinated collaboration between multiple software engineers. The organizational and communication skills required to efficiently participate in a development team are critical and distinct from basic disciplinary (i.e., programming) skills. ",
                            assessments=[ct_key_list[1]],
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c2.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form,
                            university=u.key())
        o1_2.put()

        o2_1=datamodel.Outcome(name="Theoretical Concepts",
                            index=1,
                            objective_index=2,
                            description="True competence in computer science requires not only the ability to apply known algorithms and data structures to solve a problem, but to innovatively and continually develop novel algorithms and data structures. Creating and verifying the efficiency and correctness of such novel abstractions implies a solid understanding of theoretical foundations of computer science and mathematics. ",
                            rationale="Empty",
                            assessments=[ct_key_list[0]],
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c1.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form,
                            university=u.key())
        o2_1.put()
        
        o2_2=datamodel.Outcome(name="Languages and Language Paradigms",
                            index=2,
                            objective_index=2,
                            description="A competent computer scientist must not only possess practical competence in a number of specific computer languages, but must have a broad understanding of language paradigms, abstractions shared by all computer languages, and how computer languages related and compare to each other ",
                            assessments=[ct_key_list[1]],
                            last_evaluation=datetime.datetime(2011,6,10),
                            evaluation_next=365,
                            evaluation_duration=365,
                            rationalize_course=[c2.key()],
                            rationalize_instrument=ins,
                            where_from=wiki_form,
                            university=u.key())
        o2_2.put()

        ob1=datamodel.Objective(university=u,program=p,name="Practice-Oriented Skills Requirement",description="The continual improvement of skills though practice.",index=1,outcomes=[o1_1.key(),o1_2.key()])
        ob1.put()     
        
        ob2=datamodel.Objective(university=u,program=p,name="Fundamentals",description="Make sure student does writing good.",index=2,outcomes=[o2_1.key(),o2_2.key()])
        ob2.put()   

    

        course_offerings=[(datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[0][0].key(),student_count=35,section=1,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[1][0].key(),student_count=35,section=1,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[2][0].key(),student_count=35,section=2,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[3][0].key(),student_count=35,section=2,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[4][0].key(),student_count=35,section=3,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[5][0].key(),student_count=35,section=3,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS396_WWW/syllabus.html",
                                                    course=c2,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status'])),
                          (datamodel.CourseOffering(university=u.key(),semester=s,instructor=users[6][0].key(),student_count=35,section=4,
                                                    website="http://www.cefns.nau.edu/~edo/Classes/CS315_WWW/syllabus.html",
                                                    course=c1,final_grades=['A','B','B','C','A'],tasks=['Collect Evals','Update status']))]
        
        for co in course_offerings:
            co.put()
        
        for ct,id in course_tasks:
            ct.delegates=usr_key_list
            ct.put()
        
        sl=datamodel.ScheduleLog(university=u.key(),program=p2,task=ct_key_list[0],timestamp=datetime.datetime(2012,8,15),user=usr_key_list[0],email='rmb237@nau.edu')
        sl.save()
        sl1=datamodel.ScheduleLog(university=u.key(),program=p2,task=ct_key_list[1],timestamp=datetime.datetime(2012,8,15),user=usr_key_list[1],email='jwh83@nau.edu')
        sl1.save()
               
        #c.put()
        self.response.out.write("Ok!")
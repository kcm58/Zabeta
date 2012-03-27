from google.appengine.ext import webapp, db
from dateutil.relativedelta import relativedelta
from google.appengine.api import mail
from types import *
import datamodel
import datetime
import dateutil

debug=1
deltas={}
deltas['day']=datetime.timedelta(days=1)
deltas['week']=datetime.timedelta(days=7)
deltas['month']=relativedelta(months=+1)
deltas['six_months']=relativedelta(months=+6)

class schedule(webapp.RequestHandler):
    
    def to_json(self,g):
        u_list=g.fetch(1024)
        ret=[]
        #iterate over each element returned by the select.
        for u in u_list:
            element={}
            #iterate over each parameter specified in the select
            for key in u._all_properties:
                if True:
                    try:
                        var=getattr(u,key)
                    except:
                        pass
                    if type(var) is datetime.datetime:
                        element[key]=var.isoformat("T") + "+00:00"
                    else:
                        element[key]=str(var)
                #except:
                #    pass
            ret.append(element)  
        return ret 
    
    def print_curr_task(self,task):
        #self.debug(task)
        task_str="""Task: %s <br /> 
                    Task id: %s <br />
                    Delegates: %s <br /> 
                    Begin Date: %s <br /> 
                    End Date: %s <br /> 
                    Fulfilled: %s <br /><br />""" %(task['name'],
                                                    task['id'],
                                                    task['delegates'],
                                                    task['begin_date'],
                                                    task['end_date'],
                                                    task['fulfilled'])
        self.debug(task_str)  
        
    def print_prog(self,prog):
        prog_str="""University: %s <br /> 
                    Program id: %s <br />
                    Name: %s <br /> 
                    Mission: %s <br /> 
                    Description: %s <br /> 
                    Webpage: %s <br />
                    Nag before list %s <br />
                    Nag after list %s <br /> """ %(prog['university'],
                                                   prog['id'],
                                                   prog['name'],
                                                   prog['mission'],
                                                   prog['description'],
                                                   prog['webpage'],
                                                   prog['nag_before'],
                                                   prog['nag_after'],)
        self.debug(prog_str)  
         

    def get(self): 
        #For every program:
        #pull nag list for before and after 
        #check all tasks associated with that program against nag lists
        #send necessary emails
        
        curr_date=datetime.datetime.now().date()
        curr_date_str=curr_date.isoformat()
        test_date=datetime.datetime.now().date()
        self.debug("Test date: ")
        self.debug(test_date)
        r_delta=relativedelta(months=+1)
        test_date+=r_delta
        self.debug("Test date + one month: ")
        self.debug(test_date)
        test_date=datetime.date(2012,2,15)
        self.debug("Test date: ")
        self.debug(test_date)
        r_delta=relativedelta(months=+1)
        test_date+=r_delta
        self.debug("Test date + one month: ")
        self.debug(test_date)
        self.response.out.write("<br />")
        
        progs=datamodel.Program.gql("")
        prog_list=progs.fetch(1024)
        progs_to_json=self.to_json(progs) #want to print these out
        #self.debug(progs_to_json)
        self.debug("CURRENT PROGRAMS: <br />")
        for p in progs_to_json:
            self.print_prog(p)
            
        for p in prog_list:
            #p_key=p.key()

            nag_before_dict=dict()
            nag_after_dict=dict()
            nag_before_list=p.nag_before
            nag_after_list=p.nag_after
            
            for el in nag_before_list:
                if el=="six months before":
                    nag_before_dict['six months before']=1
                elif el=="one month before":
                    nag_before_dict['one month before']=1
                elif el=="one week before":
                    nag_before_dict['one week before']=1
                elif el=="one day before":
                    nag_before_dict['one day before']=1
                    
            for el in nag_after_list:
                if el=="six months after":
                    nag_after_dict['six months after']=1
                elif el=="one month after":
                    nag_after_dict['one month after']=1
                elif el=="one week after":
                    nag_after_dict['one week after']=1
                elif el=="one day after":
                    nag_after_dict['one day after']=1 
                       
            header_str="CURRENT TASKS: %s<br />" %curr_date_str
            self.debug(header_str)
        
            curr_tasks=datamodel.CourseTask.gql("where program=:1",p)
            tasks_to_json=self.to_json(curr_tasks)
            #self.debug(tasks_to_json)
        
            for t in tasks_to_json:
                self.print_curr_task(t)
            
            self.check_expired_tasks(p)
                     
            #Check nag lists    
            self.check_nags_before(nag_before_dict,p)
            self.check_nags_after(nag_after_dict,p)
            
    def debug(self,message):
        global debug
        if debug==1:
            self.response.out.write(message)
            self.response.out.write("<br />")
            
    def check_expired_tasks(self,program):
        start_window=datetime.datetime.now().date()
        end_window=start_window+deltas['day']
        tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
        task_list=tasks.fetch(1024)
        self.debug(start_window)
        self.debug(end_window)
        for t in task_list:
            t_type=t.class_name()
            self.debug(t_type)
            self.debug(t.name)
            if t_type==datamodel.AssessmentTask:
                self.debug("Curr task is Assessment Task")
                t_copy=datamodel.AssessmentTask(university=t.University,
                                                   program=t.program,
                                                   outcome=t.outcome,
                                                   name=t.name,
                                                   fulfilled=0,
                                                   attachment_names=t.attachment_names,
                                                   attachment_blob_ids=t.attachment.blob_ids,
                                                   delegates=t.delegates)
                
                #need to update these to reflect correct values
                t_copy.begin_date=None
                t_copy.end_date=None
                #t_copy.put()
            elif t_type==datamodel.CourseTask:
                #This copy will have a empty delegates list to be updated by system later
                self.debug("Curr task is Course Task")
                t_copy=datamodel.CourseTask(university=t.university,
                                            program=t.program,
                                            course=t.course,
                                            rubric=t.rubric,
                                            name=t.name,
                                            fulfilled=0,
                                            attachment_names=t.attachment_names,
                                            attachment_blob_ids=t.attachment.blob_ids)
                
                #need to update these to reflect correct values
                t_copy.begin_date=None
                t_copy.end_date=None
                #t_copy.put()
        
    def check_nags_before(self,nag_before_dict,program):
        header_str="<br />CHECKING NAG BEFORE LIST:<br /><br />"
        self.debug(header_str)
        global deltas

        if nag_before_dict['six months before']==1:
            start_window=(datetime.datetime.now().date())+deltas['six_months']
            end_window=(start_window+deltas['six_months']+deltas['day'])
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                    self.debug("<br />")

                
        if nag_before_dict['one month before']==1:
            start_window=(datetime.datetime.now().date())+deltas['month']
            end_window=(start_window+deltas['month']+deltas['day'])
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                    self.debug("<br />")
                
        if nag_before_dict['one week before']==1:
            start_window=(datetime.datetime.now().date())+deltas['week']
            end_window=(start_window+deltas['week']+deltas['day'])
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                
        if nag_before_dict['one day before']==1:
            start_window=(datetime.datetime.now().date())+deltas['day']
            end_window=(start_window+deltas['day'])
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                    self.debug("<br />")
                
    def check_nags_after(self,nag_after_dict,program):
        header_str="<br />CHECKING NAG AFTER LIST:<br /><br />"
        self.debug(header_str)
        global deltas

        if nag_after_dict['six months after']==1:
            start_window=(datetime.datetime.now().date())-deltas['six_months']
            end_window=(start_window+deltas['day'])
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                
        if nag_after_dict['one month after']==1:
            start_window=(datetime.datetime.now().date())-deltas['month']
            end_window=(start_window+deltas['day'])
            
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                
        if nag_after_dict['one week after']==1:
            start_window=(datetime.datetime.now().date())-deltas['week']
            end_window=(start_window+deltas['day'])
            
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                
        if nag_after_dict['one day after']==1:
            start_window=(datetime.datetime.now().date())-deltas['day']
            end_window=(datetime.datetime.now().date())
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2 and program=:3",start_window,end_window,program)
            task_list=tasks.fetch(1024)
            if len(task_list)!=0:
                self.debug("Start window: ")
                self.debug(start_window)
                self.debug("End window: ")
                self.debug(end_window)
                for t in task_list:
                    t_key=t.key()
                    task_str="""Program: %s <br />
                                Task key: %s <br />
                                Task name: %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t.program.name,t_key,t.name,t.begin_date,t.end_date,t.fulfilled)
                    self.debug(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.create_schedule_log(dele,program,t)
                    
    def create_schedule_log(self,delegates,program,task):
        for d in delegates:
            new_log=datamodel.ScheduleLog(university=program.university,
                                          program=program,
                                          task=task,
                                          user=d,
                                          timestamp=datetime.datetime.now(),
                                          due_date=task.end_date,
                                          email=d.email)
            new_log.put() 
                       
    def send_emails(self,delegates,t_key):
        self.debug("Sending emails to: ")
        for d in delegates:
            self.debug(d.email)
            self.response.write(" ")
            d.email=d.email
            mail.send_mail(sender="test@zabeta.com",
                            to="%s %s"%(d.full_name,d.email),
                            subject="Test email",
                            body="""Dear %s:
                                    <a href="http://localhost:9999#%s/">Click here to view the task</a>"
                                    This is a test email.

                                    Please let me know if you got it.""" %(d.full_name,t_key))
            
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

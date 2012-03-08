from google.appengine.ext import webapp, db
from dateutil.relativedelta import relativedelta
from google.appengine.api import mail
from types import *
import datamodel
import datetime
import dateutil

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
        #self.response.out.write(task)
        task_str="""Task: %s <br /> 
                    Task id: %s <br />
                    Description: %s <br /> 
                    Delegates: %s <br /> 
                    Begin Date: %s <br /> 
                    End Date: %s <br /> 
                    Fulfilled: %s <br /><br />""" %(task['name'],
                                                    task['id'],
                                                    task['description'],
                                                    task['delegates'],
                                                    task['begin_date'],
                                                    task['end_date'],
                                                    task['fulfilled'])
        self.response.out.write(task_str)  
        
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
        self.response.out.write(prog_str)  
         

    def get(self): 
        #For every program:
        #pull nag list for before and after 
        #check all tasks associated with that program against nag lists
        #send necessary emails
        progs=datamodel.Program.gql("")
        prog_list=progs.fetch(1024)
        progs_to_json=self.to_json(progs) #want to print these out
        #self.response.out.write(progs_to_json)
        self.response.out.write("CURRENT PROGRAMS: <br /><br />")
        for p in progs_to_json:
            self.print_prog(p)
            self.response.out.write("<br />")
            
        for p in prog_list:
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
         
            curr_date=datetime.datetime.now().date()

            curr_date_str=curr_date.isoformat()
            self.response.out.write("<br />")
            test_date=datetime.datetime.now().date()
            self.response.out.write("Test date: ")
            self.response.out.write(test_date)
            self.response.out.write("<br />")
            r_delta=relativedelta(months=+1)
            test_date+=r_delta
            self.response.out.write("Test date + one month: ")
            self.response.out.write(test_date)
            self.response.out.write("<br />")
            test_date=datetime.date(2012,2,15)
            self.response.out.write("Test date: ")
            self.response.out.write(test_date)
            self.response.out.write("<br />")
            r_delta=relativedelta(months=+1)
            test_date+=r_delta
            self.response.out.write("Test date + one month: ")
            self.response.out.write(test_date)
            self.response.out.write("<br />")
            self.response.out.write("<br />")
              
            header_str="CURRENT TASKS: %s<br /><br />" %curr_date_str
            self.response.out.write(header_str)
        
            curr_tasks=datamodel.CourseTask.gql("")
            tasks_to_json=self.to_json(curr_tasks)
        
            for t in tasks_to_json:
                self.print_curr_task(t)
                     
            #Check nag lists    
            self.check_nags_before(nag_before_dict)
            self.check_nags_after(nag_after_dict)
        
    def check_nags_before(self,nag_before_dict):
        header_str="<br />CHECKING NAG BEFORE LIST:<br /><br />"
        self.response.out.write(header_str)
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=relativedelta(months=+1)
        deltas['six_months']=relativedelta(months=+6)

        if nag_before_dict['six months before']==1:
            start_window=(datetime.datetime.now().date())+deltas['six_months']
            end_window=(start_window+deltas['six_months']+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                t_key=t.key()
                task_str="""Task key: %s <br />
                            Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                self.send_emails(dele,t_key)
                self.response.out.write("<br />")

                
        if nag_before_dict['one month before']==1:
            start_window=(datetime.datetime.now().date())+deltas['month']
            end_window=(start_window+deltas['month']+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
        if nag_before_dict['one week before']==1:
            start_window=(datetime.datetime.now().date())+deltas['week']
            end_window=(start_window+deltas['week']+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
        if nag_before_dict['one day before']==1:
            start_window=(datetime.datetime.now().date())+deltas['day']
            end_window=(start_window+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
    def check_nags_after(self,nag_after_dict):
        header_str="<br />CHECKING NAG AFTER LIST:<br /><br />"
        self.response.out.write(header_str)
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=relativedelta(months=+1)
        deltas['six_months']=relativedelta(months=+6)

        if nag_after_dict['six months after']==1:
            start_window=(datetime.datetime.now().date())-deltas['six_months']
            end_window=(start_window+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
        if nag_after_dict['one month after']==1:
            start_window=(datetime.datetime.now().date())-deltas['month']
            end_window=(start_window+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
        if nag_after_dict['one week after']==1:
            start_window=(datetime.datetime.now().date())-deltas['week']
            end_window=(start_window+deltas['day'])
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
        if nag_after_dict['one day after']==1:
            start_window=(datetime.datetime.now().date())-deltas['day']
            end_window=(datetime.datetime.now().date())
            self.response.out.write("Start window: ")
            self.response.out.write(start_window)
            self.response.write("<br />")
            self.response.out.write("End window: ")
            self.response.out.write(end_window)
            self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                if t.fulfilled==0:
                    t_key=t.key()
                    task_str="""Task key: %s <br />
                                Task name: %s <br /> 
                                Task description %s <br /> 
                                Begin date: %s <br /> 
                                End date: %s <br /> 
                                Fulfilled?: %s <br />""" %(t_key,t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                    self.response.out.write(task_str)
                    dele=db.get(t.delegates)
                    self.send_emails(dele,t_key)
                    self.response.out.write("<br />")
                
    def send_emails(self,delegates,t_key):
        self.response.out.write("Sending emails to: ")
        for d in delegates:
            self.response.out.write(d.email)
            self.response.write(" ")
            d_full_name=d.full_name
            d.email=d.email
            mail.send_mail(sender="test@zabeta.com",
                            to="%s %s"%(d.full_name,d.email),
                            subject="Test email",
                            body="""Dear %s:
                                    <a href="http://localhost:9999#%s/">Click here to view the task</a>"
                                    This is a test email.

                                    Please let me know if you got it.""" %(d.full_name,t_key))
        self.response.out.write("<br />")
       
    def interpret_delta(self,str):
        print ""
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

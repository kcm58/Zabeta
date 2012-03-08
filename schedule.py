from google.appengine.ext import webapp, db
from types import *
import datamodel
import datetime
import dateutil
from dateutil.relativedelta import relativedelta
from google.appengine.api import mail


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
        task_str="""Task: %s <br /> Description: %s <br /> 
                    Delegates: %s <br /> 
                    Begin Date: %s <br /> 
                    End Date: %s <br /> 
                    Fulfilled: %s <br /><br />""" %(task['name'],
                                                  task['description'],
                                                  task['delegates'],
                                                  task['begin_date'],
                                                  task['end_date'],
                                                  task['fulfilled'])
        self.response.out.write(task_str)    

    def get(self): 
        
        #TODO: For every program, pull nag list for before and after, and check all tasks associated with that program against nag lists
        
        #Example nag before list
        nag_before_dict=dict()
        nag_before_dict['six months before']=1
        nag_before_dict['one month before']=1
        nag_before_dict['one week before']=1
        nag_before_dict['one day before']=1 
        nag_before_dict['day of']=1
        
        #Example nag after list
        nag_after_dict=dict()
        nag_after_dict['six months after']=1
        nag_after_dict['one month after']=1
        nag_after_dict['one week after']=1
        nag_after_dict['one day after']=1 
         
        curr_date=datetime.datetime.now().date()
        if type(curr_date) is NoneType:
            self.response.out.write("F_Bomb")
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
            #self.response.out.write(start_window)
            #self.response.write("<br />")
            #self.response.out.write(end_window)
            #self.response.write("<br />")
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")
                
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
                task_str="""Task name: %s <br /> 
                            Task description %s <br /> 
                            Begin date: %s <br /> 
                            End date: %s <br /> 
                            Fulfilled?: %s <br />
                            Delegate emails: """ %(t.name,t.description,t.begin_date,t.end_date,t.fulfilled)
                self.response.out.write(task_str)
                dele=db.get(t.delegates)
                for d in dele:
                    self.response.out.write(d.email)
                    self.response.write(" ")
                    d_full_name=d.full_name
                    d.email=d.email
                    mail.send_mail(sender="test@zabeta.com",
                                   to="%s %s"%(d.full_name,d.email),
                                   subject="Test email",
                                   body="""Dear %s:

                                           This is a test email.

                                           Please let me know if you got it.""" %d.full_name)
                self.response.write("one day <br />")
                self.response.write("<br />")

        
        
        
        
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

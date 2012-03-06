from google.appengine.ext import webapp, db
from types import *
import datamodel
import datetime
import dateutil
from dateutil.relativedelta import relativedelta


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
        begin_date_ls=task['begin_date'].split(':')
        begin_date=begin_date_ls[0].rstrip('T00')
        end_date_ls=task['end_date'].split(':')
        end_date=end_date_ls[0].rstrip('T00')
        task_str="""Task: %s <br /> Description: %s <br /> 
                    Delegates: %s <br /> 
                    Begin Date: %s <br /> 
                    End Date: %s <br /> 
                    Fulfilled: %s <br /><br />""" %(task['name'],
                                                  task['description'],
                                                  task['delegates'],
                                                  begin_date,end_date,
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
        self.check_nags_before2(nag_before_dict)
        #self.check_nags_after2(task_list,nag_after_dict)
        
    def check_nags_before2(self,nag_before_dict):
        header_str="<br />CHECKING NAG BEFORE LIST:<br />"
        self.response.out.write(header_str)
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=relativedelta(months=+1)
        deltas['six_months']=relativedelta(months=+6)
        curr_date=datetime.datetime.now()
        curr_date_test=datetime.date(2011,12,15)

        if nag_before_dict['six months before']==1:
            start_window=(datetime.datetime.now().date())-deltas['six_months']#+six_month_delta
            end_window=(datetime.datetime.now().date())-deltas['six_months']+deltas['day']
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                dele=db.get(t.delegates)
                self.response.out.write(dele[0].email)
                self.response.write("six months <br />")
                self.response.write("<br />")
                
        if nag_before_dict['one month before']==1:
            start_window=(datetime.datetime.now().date())-deltas['month']#+six_month_delta
            end_window=(datetime.datetime.now().date())-deltas['month']+deltas['day']
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                dele=db.get(t.delegates)
                self.response.out.write(dele[0].email)
                self.response.write("one month <br />")

                self.response.write("<br />")
                
        if nag_before_dict['one week before']==1:
            start_window=(datetime.datetime.now().date())-deltas['week']#+six_month_delta
            end_window=(datetime.datetime.now().date())-deltas['week']+deltas['day']
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                dele=db.get(t.delegates)
                self.response.out.write(dele[0].email)
                self.response.write("one week <br />")

                self.response.write("<br />")
                
        if nag_before_dict['one day before']==1:
            start_window=(datetime.datetime.now().date())-deltas['day']#+six_month_delta
            end_window=(datetime.datetime.now().date())
            tasks=datamodel.CourseTask.gql("where end_date>:1 and end_date<:2",start_window,end_window)
            task_list=tasks.fetch(1024)
            for t in task_list:
                dele=db.get(t.delegates)
                self.response.out.write(dele[0].email)
                self.response.write("one day <br />")

                self.response.write("<br />")
            
         
    #Given: a nag_list object representing all the times to nag after a task is due
    #Given: a list of tasks to check
    #Create a list of deltas to add/subtract from current date
    #Check nag list flags and add deltas from current date to see if it is time to nag
    def check_nags_after2(self,task_list,nag_after_dict):
        header_str="CHECKING NAG AFTER LIST:<br />"
        self.response.out.write(header_str)
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=datetime.timedelta(days=31)
        curr_date=datetime.datetime.now().date()
        curr_date_test=datetime.date(2012,12,18) #Use this to debug
        curr_date_test_str=""
        curr_date_test_str+=str(curr_date_test.year)
        curr_date_test_str+="-"
        curr_date_test_str+=str(curr_date_test.month)
        curr_date_test_str+="-"
        curr_date_test_str+=str(curr_date_test.day)
        self.response.out.write("Using %s as current date for debugging <br /><br />" %curr_date_test_str)
        
        for t in range(0,len(task_list)):
            begin_date_ls=task_list[t]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=task_list[t]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="""Task: %s <br /> Description: %s <br /> 
                        Delegates: %s <br /> 
                        Current Date: %s <br /> 
                        Begin Date: %s <br /> 
                        End Date: %s <br /> 
                        Fulfilled: %s <br />""" %(task_list[t]['name'],
                                                  task_list[t]['description'],
                                                  task_list[t]['delegates'],
                                                  curr_date_test,begin_date,end_date,
                                                  task_list[t]['fulfilled'])
                                                                                                                                                          
            self.response.out.write(task_str)
            end_date_ls=end_date.split('-')
            end_date_obj=datetime.date(int(end_date_ls[0]),int(end_date_ls[1]),int(end_date_ls[2]))
            if nag_after_dict['six months after']==1 and int(task_list[t]['fulfilled'])==0:
                six_months_after=end_date_obj+(6*deltas['month'])
                if curr_date_test==six_months_after:
                    self.response.out.write("Need to nag at 6 months after! <br />")
            if nag_after_dict['one month after']==1 and int(task_list[t]['fulfilled'])==0:
                one_week_month=end_date_obj+deltas['month']
                if curr_date_test==one_week_month:
                    self.response.out.write("Need to nag at 1 month after! <br />")
            if nag_after_dict['one week after']==1 and int(task_list[t]['fulfilled'])==0:
                one_week_after=end_date_obj+deltas['week']
                if curr_date_test==one_week_after:
                    self.response.out.write("Need to nag at 1 week after! <br />")
            if nag_after_dict['one day after']==1 and int(task_list[t]['fulfilled'])==0:
                one_day_after=end_date_obj+deltas['day']
                if curr_date_test==one_day_after:
                    self.response.write("Need to nag at one day after! <br />")
                    
            self.response.out.write("<br />")
            
            

                    
            

        
        
        
        
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

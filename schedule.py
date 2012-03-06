from google.appengine.ext import webapp, db
from types import *
import datamodel
import datetime


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
        header_str="CURRENT TASKS: %s<br /><br />" %curr_date_str
        self.response.out.write(header_str)
        curr_tasks=datamodel.CourseTask.gql("")
        tasks_to_json=self.to_json(curr_tasks)
        
        #Used for debugging: just print out all tasks
        for i in range(0,len(tasks_to_json)): 
            begin_date_ls=tasks_to_json[i]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=tasks_to_json[i]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="Task: %s <br /> Description: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br /><br />" %(tasks_to_json[i]['name'],
                                                                                                                                                          tasks_to_json[i]['description'],
                                                                                                                                                          tasks_to_json[i]['delegates'],
                                                                                                                                                          begin_date,end_date,
                                                                                                                                                          tasks_to_json[i]['fulfilled'])
            self.response.out.write(task_str)
        
        #Check nag lists    
        self.check_nags_before(tasks_to_json,nag_before_dict)
        self.check_nags_after(tasks_to_json,nag_after_dict)
             
    #Given: a nag_list object representing all the times to nag before a task is due
    #Given: a list of tasks to check
    #Create a list of deltas to add/subtract from current date
    #Check nag list flags and subtract deltas from current date to see if it is time to nag
    def check_nags_before(self,task_list,nag_before_dict):
        header_str="CHECKING NAG BEFORE LIST:<br />"
        self.response.out.write(header_str)
        deltas={}
        deltas['day']=datetime.timedelta(days=1)
        deltas['week']=datetime.timedelta(days=7)
        deltas['month']=datetime.timedelta(days=31)
        curr_date=datetime.datetime.now().date()
        curr_date_test=datetime.date(2012,06,14) #Use this to debug
        curr_date_test_str=""
        curr_date_test_str+=str(curr_date_test.year)
        curr_date_test_str+="-"
        curr_date_test_str+=str(curr_date_test.month)
        curr_date_test_str+="-"
        curr_date_test_str+=str(curr_date_test.day)
        self.response.out.write("Using %s as current date for testing <br /><br />" %curr_date_test_str)
        
        for t in range(0,len(task_list)):
            begin_date_ls=task_list[t]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=task_list[t]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="Task: %s <br /> Description: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br />" %(task_list[t]['name'],
                                                                                                                                                          task_list[t]['description'],
                                                                                                                                                          task_list[t]['delegates'],
                                                                                                                                                          begin_date,end_date,
                                                                                                                                                          task_list[t]['fulfilled'])
            self.response.out.write(task_str)
            end_date_ls=end_date.split('-')
            end_date_obj=datetime.date(int(end_date_ls[0]),int(end_date_ls[1]),int(end_date_ls[2]))
            if nag_before_dict['six months before']==1 and int(task_list[t]['fulfilled'])==0:
                six_months_before=end_date_obj-(6*deltas['month'])
                if curr_date_test==six_months_before:
                    self.response.out.write("Need to nag at 6 months before! <br />")
            if nag_before_dict['one month before']==1 and int(task_list[t]['fulfilled'])==0:
                one_month_before=end_date_obj-deltas['month']
                if curr_date_test==one_month_before:
                    self.response.out.write("Need to nag at 1 month before! <br />")
            if nag_before_dict['one week before']==1 and int(task_list[t]['fulfilled'])==0:
                one_week_before=end_date_obj-deltas['week']
                if curr_date_test==one_week_before:
                    self.response.out.write("Need to nag at 1 week before! <br />")
            if nag_before_dict['one day before']==1 and int(task_list[t]['fulfilled'])==0:
                one_day_before=end_date_obj-deltas['day']
                if curr_date_test==one_day_before:
                    self.response.write("Need to nag at one day before! <br />")
            if nag_before_dict['day of']==1 and int(task_list[t]['fulfilled'])==0:
                if curr_date_test==end_date_obj:
                    self.response.write("Need to nag on day of! <br />")
                    
            date_diff=(end_date_obj-curr_date).days
            self.response.out.write("Difference in curr date and task end date: %s <br /><br />" %date_diff)
            
    #Given: a nag_list object representing all the times to nag after a task is due
    #Given: a list of tasks to check
    #Create a list of deltas to add/subtract from current date
    #Check nag list flags and add deltas from current date to see if it is time to nag
    def check_nags_after(self,task_list,nag_after_dict):
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
        self.response.out.write("Using %s as current date for testing <br /><br />" %curr_date_test_str)
        self.response.out.write("Using %s as current date for debugging")
        
        for t in range(0,len(task_list)):
            begin_date_ls=task_list[t]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=task_list[t]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="Task: %s <br /> Description: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br />" %(task_list[t]['name'],
                                                                                                                                                          task_list[t]['description'],
                                                                                                                                                          task_list[t]['delegates'],
                                                                                                                                                          begin_date,end_date,
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
                    
            

        
        
        
        
        
        
       
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    

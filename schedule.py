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
        #self.response.out.write("run schedule")
        curr_date=datetime.datetime.now().date()
        if type(curr_date) is NoneType:
            self.respons.out.write("F_Bomb")
        curr_date_str=curr_date.isoformat()
        header_str="CURRENT TASKS: %s<br /><br />" %curr_date_str
        self.response.out.write(header_str)
        curr_tasks=datamodel.CourseTask.gql("")
        tasks_to_json=self.to_json(curr_tasks)
        
        for i in range(0,len(tasks_to_json)): 
            begin_date_ls=tasks_to_json[i]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=tasks_to_json[i]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="Task: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br /><br />" %(tasks_to_json[i]['name'],
                                                                                                                                   tasks_to_json[i]['delegates'],
                                                                                                                                   begin_date,end_date,
                                                                                                                                   tasks_to_json[i]['fulfilled'])
            self.response.out.write(task_str)
            
        self.response.out.write("GETTING ALL TASKS ASSOCIATED WITH DATE: %s<br />" %curr_date)
        for i in range(0,len(tasks_to_json)): 
            begin_date_ls=tasks_to_json[i]['begin_date'].split(':')
            begin_date=begin_date_ls[0].rstrip('T00')
            end_date_ls=tasks_to_json[i]['end_date'].split(':')
            end_date=end_date_ls[0].rstrip('T00')
            task_str="Task: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br /><br />" %(tasks_to_json[i]['name'],
                                                                                                                                   tasks_to_json[i]['delegates'],
                                                                                                                                   begin_date,end_date,
                                                                                                                                   tasks_to_json[i]['fulfilled'])
        #self.response.out.write(tasks_to_json[1])
        
        
    

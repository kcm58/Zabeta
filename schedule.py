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

    def get(self,):    
        #self.response.out.write("run schedule")
        curr_date=datetime.datetime.now().date()
        if type(curr_date) is NoneType:
            self.respons.out.write("Fuck")
        #self.response.out.write(curr_date)
        curr_tasks=datamodel.CourseTask.gql("")
        tasks_to_json=self.to_json(curr_tasks)
        #self.response.write("CURRENT TASKS: %s <br />") %curr_date
        #begin_date=tasks_to_json[i]['begin_date']   
        #end_date=tasks_to_json[i]['end_date']
        #range_str="Range: %s - %s<br /><br />" %(begin_date,end_date)
        for i in range(0,len(tasks_to_json)): 
            #self.response.out.write(range_str)
            task_str="Task: %s <br /> Delegates: %s <br /> Begin Date: %s <br /> End Date: %s <br /> Fulfilled: %s <br /><br />" %(tasks_to_json[i]['name'],
                                                                                                                                   tasks_to_json[i]['delegates'],
                                                                                                                                   tasks_to_json[i]['begin_date'],
                                                                                                                                   tasks_to_json[i]['end_date'],
                                                                                                                                   tasks_to_json[i]['fulfilled'])
            self.response.out.write(task_str)
        #self.response.out.write(tasks_to_json[1])
        
        
    

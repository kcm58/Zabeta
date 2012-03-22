import api
from google.appengine.ext import db
import datamodel
import json
import urllib2

class list(api.api):
    public={"University":True,
            "Program":True,
            "Task":True,
            "AssessmentTask":True,
            "CourseTask":True,
            "Semester":True,
            "CourseOffering":True,
            "Course":True,
            "Instrument":True,
            "Outcome":True,
            "Objective":True,
            "Minutes":True,
            "ScheduleLog":True,
            "User":True,
            "Batch":True,
            "EmailLog":True,
            }
    
    #takes in a collection and makes sure to only pull out records the user has access to.
    def filter(self,collection):
        return collection.gql("where university=key(:1) and program=key(:2)",self.university_id,self.program_id)

    def University(self):
        #"where university=:1",self.university
        return self.filter(datamodel.University)

    def Program(self):      
        return self.filter(datamodel.Program)

    def CourseTask(self):
        return self.filter(datamodel.CourseTask)

    def Task(self):
        return self.filter(datamodel.Task)

    def AssessmentTask(self):
        return self.filter(datamodel.AssessmentTask)

    def Semester(self):
        return self.filter(datamodel.Semester)

    def CourseOffering(self):
        return self.filter(datamodel.CourseOffering)

    def Course(self):
        return self.filter(datamodel.Course)

    def Instrument(self):
        return self.filter(datamodel.Instrument)

    def Outcome(self,assessment=False):
        if assessment:
            ret = datamodel.Outcome.gql("where university=key(:1) and program=key(:2) and assessments=KEY(:3)",self.university_id, self.program_id, assessment)
        else:
            ret = self.filter(datamodel.Outcome)
        return ret
      
    def Objective(self):
        return self.filter(datamodel.Objective)

    def Minutes(self,program):
        return self.filter(datamodel.Minutes)

    def ScheduleLog(self,program):
        return self.filter(datamodel.ScheduleLog)

    def User(self):
        return self.filter(datamodel.User)
    
    def EmailLog(self):
        return self.filter(datamodel.EmailLog)
    
    #Accepts a post body of json and returns the list of keys.
    def Batch(self):
        j=urllib2.unquote(self.request.body)
        keys=json.loads(j)
        return db.get(keys)

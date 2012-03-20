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

    def University(self):
        #"where university=:1",self.university
        return datamodel.University.all()

    def Program(self):      
        return datamodel.Program.all()

    def CourseTask(self):
        return datamodel.CourseTask.all()

    def Task(self):
        return datamodel.Task.all()

    def AssessmentTask(self):
        return datamodel.AssessmentTask.all()

    def Semester(self):
        return datamodel.Semester.all()

    def CourseOffering(self):
        return datamodel.CourseOffering.all()

    def Course(self):
        return datamodel.Course.all()

    def Instrument(self):
        return datamodel.Instrument.all()

    def Outcome(self,assessment=False):
        if assessment:
            ret = datamodel.Outcome.gql("where assessments=KEY(:1)",assessment)
        else:
            ret = datamodel.Outcome.all()
        return ret
      
    def Objective(self):
        return datamodel.Objective.all()

    def Minutes(self,program):
        return datamodel.Minutes.all()

    def ScheduleLog(self,program):
        return datamodel.ScheduleLog.all()

    def User(self):
        return datamodel.User.all()
    
    def EmailLog(self):
        return datamodel.EmailLog.all()
    
    #Accepts a post body of json and returns the list of keys.
    def Batch(self):
        j=urllib2.unquote(self.request.body)
        keys=json.loads(j)
        return db.get(keys)

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
            "Batch":True
            }

    def University(self):
        #"where university=:1",self.university
        return datamodel.University.gql("")

    def Program(self):
        return datamodel.Program.gql("")

    def CourseTask(self):
        return datamodel.CourseTask.gql("")

    def Task(self):
        return datamodel.Task.gql("")

    def AssessmentTask(self):
        return datamodel.AssessmentTask.gql("")

    def Semester(self):
        return datamodel.Semester.gql("")

    def CourseOffering(self):
        return datamodel.CourseOffering.gql("")

    def Course(self):
        return datamodel.Course.gql("")

    def Instrument(self):
        return datamodel.Instrument.gql("")

    def Outcome(self):
        return datamodel.Outcome.gql("")

    def Objective(self):
        return datamodel.Objective.gql("")

    def Minutes(self,program):
        return datamodel.Minutes.gql("")

    def ScheduleLog(self,program):
        return datamodel.ScheduleLog.gql("")

    def User(self):
        return datamodel.User.gql("")

    #Accepts a post body of json and returns the list of keys. 
    def Batch(self):
        j=urllib2.unquote(self.request.body)
        keys=json.loads(j)
        return db.get(keys)

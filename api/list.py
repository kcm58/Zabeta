import api
from google.appengine.ext import db
import datamodel

class list(api.api):
    public={"University":True,
            "Program":True,
            "Task":True,
            "CourseTask":True,
            "Semester":True,
            "CourseOffering":True,
            "Course":True,
            "Instrument":True,
            "Outcome":True,
            "Objective":True,
            "Minutes":True,}

    def University(self):
        #"where university=:1",self.university
        return datamodel.University.gql("")

    def Program(self):
        return datamodel.Program.gql("")

    def Task(self):
        return datamodel.CourseTask.gql("")

    def CourseTask(self):
        return datamodel.CourseTask.gql("")

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
        return datamodel.Objective.gql("").filter('program =', program)

